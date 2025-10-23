
import random
import time
import sys

# Config
QUARTER_LENGTH_SECONDS = 60  # Real seconds for demo; treat as 15-minute quarters compressed
TEAM_NAMES = ("Home Hawks", "Away Bears")
FIELD_LENGTH = 100  # yards
TOUCHDOWN_YARDS = 100
START_POSITION = 25  # start at own 25 after kickoff
KICKOFF_TOUCHBACK_POS = 25
FIELD_GOAL_MAX_RANGE = 55  # yards (kick + endzone + placement)
VERBOSE = False  # toggle for debugging internal values


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.possessions = 0

    def __str__(self):
        return f"{self.name} ({self.score})"


class Game:
    def __init__(self, home_name=TEAM_NAMES[0], away_name=TEAM_NAMES[1]):
        self.home = Team(home_name)
        self.away = Team(away_name)
        self.quarter = 1
        self.clock = QUARTER_LENGTH_SECONDS
        self.possession = self.home  # home starts with the ball
        self.ball_position = START_POSITION  # yards from offense's own goal line (0 = own goal line)
        self.down = 1
        self.to_go = 10
        self.attempt = 0
        self.play_log = []
        self.game_over = False
        self.kickoff_next_to = self.away  # who will receive kickoff? not used heavily

    def other_team(self, team):
        return self.away if team is self.home else self.home

    def log(self, s):
        ts = f"[Q{self.quarter} {self.clock}s]"
        line = f"{ts} {s}"
        self.play_log.append(line)
        print(line)

    def kickoff(self):
        # Simple kickoff, touchback to 25
        self.ball_position = KICKOFF_TOUCHBACK_POS
        self.down = 1
        self.to_go = 10
        self.possession = self.other_team(self.possession)
        self.log(f"Kickoff! {self.possession.name} receives at the {self.ball_position}.")

    def end_quarter_check(self):
        if self.clock <= 0:
            if self.quarter >= 4:
                self.game_over = True
                self.log("End of regulation.")
            else:
                self.quarter += 1
                self.clock = QUARTER_LENGTH_SECONDS
                self.log(f"End of quarter. Starting Q{self.quarter}.")
                # Switch kickoff possession
                self.possession = self.other_team(self.possession)
                self.kickoff()

    def advance_clock(self, seconds):
        self.clock -= seconds
        if self.clock < 0:
            self.clock = 0

    def score_touchdown(self, team):
        team.score += 6
        self.log(f"TOUCHDOWN! {team.name} scores 6 points. Score: {self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        # extra point attempt (automatic 1)
        team.score += 1
        self.log(f"Extra point good. {team.name} +1 (automatic). Score now: {self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        # kickoff afterward: other team receives at 25
        self.possession = self.other_team(team)
        self.ball_position = KICKOFF_TOUCHBACK_POS
        self.down = 1
        self.to_go = 10

    def score_field_goal(self, team):
        team.score += 3
        self.log(f"Field goal! {team.name} +3. Score now: {self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        self.possession = self.other_team(team)
        self.ball_position = KICKOFF_TOUCHBACK_POS
        self.down = 1
        self.to_go = 10

    def safety(self, defense_team):
        defense_team.score += 2
        self.log(f"SAFETY! {defense_team.name} +2. Score now: {self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        # possession changes: team that was awarded safety kicks to other team; we'll give ball to defense at 25
        self.possession = defense_team
        self.ball_position = KICKOFF_TOUCHBACK_POS
        self.down = 1
        self.to_go = 10

    def attempt_play(self, play_choice, is_player=True):
        # play_choice: "run", "short", "deep", "punt", "fg"
        offense = self.possession
        defense = self.other_team(offense)
        self.attempt += 1

        # base yard ranges & turnover probabilities
        outcome = {
            "yards": 0,
            "turnover": False,
            "safety": False,
            "scoring": None,
            "clock": random.randint(5, 15),
            "description": ""
        }

        distance_modifier = clamp(10 - self.to_go, -5, 5)

        if play_choice == "run":
            yards = random.randint(-2, 8) + int(distance_modifier * 0.5)
            fumble = random.random() < 0.03
            if fumble:
                outcome["turnover"] = True
                outcome["yards"] = -abs(random.randint(0, 10))
                outcome["description"] = f"Fumble! Recovered by {defense.name}."
            else:
                outcome["yards"] = yards
                outcome["description"] = f"Run for {yards} yards."
        elif play_choice == "short":
            yards = random.randint(-1, 18) + int(distance_modifier)
            interception = random.random() < 0.05
            if interception:
                outcome["turnover"] = True
                outcome["description"] = f"Short pass intercepted by {defense.name}!"
                outcome["yards"] = -abs(random.randint(0, 30))
            else:
                outcome["yards"] = yards
                outcome["description"] = f"Short pass complete for {yards} yards."
        elif play_choice == "deep":
            yards = random.randint(-10, 40) + int(distance_modifier * 2)
            interception = random.random() < 0.12
            if interception:
                outcome["turnover"] = True
                outcome["description"] = f"Deep pass intercepted by {defense.name}!"
                outcome["yards"] = -abs(random.randint(0, 50))
            else:
                outcome["yards"] = yards
                outcome["description"] = f"Deep pass caught for {yards} yards."
        elif play_choice == "punt":
            punt_dist = random.randint(30, 55)
            old_pos = self.ball_position
            new_pos = clamp(FIELD_LENGTH - (old_pos + punt_dist), 10, FIELD_LENGTH - 10)
            outcome["turnover"] = True
            outcome["yards"] = -(punt_dist)
            outcome["description"] = f"Punt of {punt_dist} yards. Ball to {defense.name} at their {new_pos}."
            outcome["punt_newpos"] = new_pos
        elif play_choice == "fg":
            distance_to_goal = FIELD_LENGTH - self.ball_position + 10
            base_chance = 0.95 - (distance_to_goal - 20) * 0.015
            base_chance = clamp(base_chance, 0.05, 0.98)
            success = random.random() < base_chance
            outcome["clock"] = random.randint(3, 7)
            if success:
                outcome["scoring"] = "FG"
                outcome["description"] = f"Field goal from {distance_to_goal} yards is GOOD."
                self.score_field_goal(offense)
            else:
                outcome["description"] = f"Field goal from {distance_to_goal} yards is NO GOOD."
                outcome["turnover"] = True
            return outcome

        old_pos = self.ball_position
        self.ball_position += outcome["yards"]

        if self.ball_position <= 0:
            outcome["safety"] = True
            outcome["description"] += " Ball in own endzone! Safety."
            self.safety(defense)
            return outcome

        if self.ball_position >= FIELD_LENGTH:
            self.score_touchdown(offense)
            outcome["scoring"] = "TD"
            return outcome

        self.advance_clock(outcome["clock"])

        if outcome["turnover"]:
            self.possession = defense
            new_pos = clamp(FIELD_LENGTH - max(20, abs(outcome["yards"])), 20, FIELD_LENGTH - 1)
            self.ball_position = new_pos
            self.down = 1
            self.to_go = 10
            self.log(outcome["description"])
            self.end_quarter_check()
            return outcome

        gained = outcome["yards"]
        if gained >= self.to_go:
            self.down = 1
            self.to_go = 10
            self.log(outcome["description"] + " — First down!")
        else:
            self.down += 1
            self.to_go = max(1, self.to_go - gained)
            self.log(outcome["description"] + f" — {self.down} and {self.to_go} at the {self.ball_position}.")

        if self.ball_position >= FIELD_LENGTH:
            self.score_touchdown(offense)
            outcome["scoring"] = "TD"
            return outcome

        if self.down > 4:
            self.possession = defense
            self.ball_position = FIELD_LENGTH - self.ball_position
            self.down = 1
            self.to_go = 10
            self.log(f"Turnover on downs. Ball to {self.possession.name} at the {self.ball_position}.")
            self.end_quarter_check()
            return outcome

        self.end_quarter_check()
        return outcome

    def cpu_decide(self):
        if self.down == 4:
            distance_to_goal = FIELD_LENGTH - self.ball_position + 10
            if distance_to_goal <= FIELD_GOAL_MAX_RANGE and random.random() < 0.6:
                return "fg"
            if self.ball_position < 50 and random.random() < 0.8:
                return "punt"
            if self.to_go <= 3:
                return "short" if random.random() < 0.8 else "deep"
            else:
                return "deep" if random.random() < 0.5 else "short"
        else:
            if self.to_go <= 3:
                return "run" if random.random() < 0.6 else "short"
            if self.to_go <= 7:
                return "short" if random.random() < 0.7 else "deep"
            return "deep" if random.random() < 0.5 else "short"

    def display_status(self):
        print("\n" + "=" * 50)
        print(f"Q{self.quarter} | {self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        print(f"Time: {self.clock}s | Possession: {self.possession.name}")
        print(f"Ball on: {self.ball_position} | Down: {self.down} | To Go: {self.to_go}")
        print("=" * 50 + "\n")

    def user_turn(self):
        self.display_status()
        print("Choose your play:")
        print(" 1) Run")
        print(" 2) Short Pass")
        print(" 3) Deep Pass")
        print(" 4) Punt")
        print(" 5) Field Goal Attempt")
        choice = input("> ").strip()
        mapping = {"1": "run", "2": "short", "3": "deep", "4": "punt", "5": "fg"}
        return mapping.get(choice, "run")

    def run_game(self):
        self.log("Game start!")
        self.kickoff()
        while not self.game_over:
            is_player = (self.possession is self.home)
            play = self.user_turn() if is_player else self.cpu_decide()

            if play == "fg":
                distance_to_goal = FIELD_LENGTH - self.ball_position + 10
                if distance_to_goal > FIELD_GOAL_MAX_RANGE and is_player:
                    print(f"Too far for a realistic field goal ({distance_to_goal}y). Try again.")
                    play = self.user_turn()

            self.attempt_play(play, is_player=is_player)
            time.sleep(0.25)

        print("\n" + "=" * 70)
        print("Final Score:")
        print(f"{self.home.name} {self.home.score} - {self.away.score} {self.away.name}")
        print("Play-by-play:")
        for line in self.play_log:
            print(line)
        print("=" * 70)


def main():
    print("Welcome to CLI Football!\n")
    home = input("Enter your team name (or press Enter for 'Home Hawks'): ").strip() or TEAM_NAMES[0]
    away = input("Enter opponent name (or press Enter for 'Away Bears'): ").strip() or TEAM_NAMES[1]
    game = Game(home_name=home, away_name=away)
    try:
        game.run_game()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        print(f"Score: {game.home.name} {game.home.score} - {game.away.score} {game.away.name}")
        sys.exit(0)


if __name__ == '__main__':
    main()
