# Hidden Movement

Hidden Movement is a theory which provides the dataset routinely moves around in distinct pathways to determine the readability and accuracy of in basketball. These are often deployed to predict the rate of such elements from the game and the rate it can produce such events

## Example code

import random

-- Define possible basketball events -- 
events = ["shot_made", "shot_missed", "pass_success", "pass_fail", "turnover"]

class HiddenMovementBasketball:
    def __init__(self, num_events=50):
        self.num_events = num_events
        self.dataset = []
        self.pathways = []  # Simulate movement paths of events
    
    def generate_event(self):
        """Simulate an event with some weighted probabilities."""
        weights = [0.45, 0.25, 0.2, 0.05, 0.05]  # Probabilities for each event
        return random.choices(events, weights)[0]

    def simulate_dataset(self):
        """Generate dataset and track hidden movement pathways."""
        for _ in range(self.num_events):
            event = self.generate_event()
            # Assign a "hidden pathway" (a random route the data might take internally)
            pathway = random.randint(1, 5)
            self.dataset.append((event, pathway))
            self.pathways.append(pathway)

    def analyze_dataset(self):
        """Analyze dataset to determine frequency and predictive value of events."""
        event_count = {e: 0 for e in events}
        pathway_count = {i: 0 for i in range(1, 6)}

        for event, pathway in self.dataset:
            event_count[event] += 1
            pathway_count[pathway] += 1

        print("Event Frequencies:")
        for e, count in event_count.items():
            print(f"{e}: {count} ({count/self.num_events:.2%})")
        
        print("\nHidden Pathway Frequencies:")
        for p, count in pathway_count.items():
            print(f"Pathway {p}: {count} ({count/self.num_events:.2%})")

    def predict_next_event(self):
        """Predict next event based on most frequent previous events in a pathway."""
        pathway_events = {}
        for event, pathway in self.dataset:
            if pathway not in pathway_events:
                pathway_events[pathway] = []
            pathway_events[pathway].append(event)
        
        predictions = {}
        for pathway, events_list in pathway_events.items():
            # Predict most common event in this pathway
            prediction = max(set(events_list), key=events_list.count)
            predictions[pathway] = prediction
        
        print("\nPredicted Next Event per Pathway:")
        for p, pred in predictions.items():
            print(f"Pathway {p} → {pred}")


 -- Run the Hidden Movement Simulation --
 hidden_movement = HiddenMovementBasketball(num_events=100)
 hidden_movement.simulate_dataset()
 hidden_movement.analyze_dataset()
 hidden_movement.predict_next_event()