import java.util.Scanner;

public class NucleusPlay {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        while (running) {
            System.out.println("\n=== traMap ===");
            System.out.println("[1] Basketball Wordle");
            System.out.println("[2] Country Trivia");
            System.out.println("[3] Game Tip of the Day");
            System.out.println("[0] Exit");

            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1 -> basketballWordle(scanner);
                case 2 -> countryTrivia(scanner);
                case 3 -> gameTip();
                case 0 -> {
                    System.out.println("Goodbye from Nucleus Play!");
                    running = false;
                }
                default -> System.out.println("Invalid option.");
            }
        }
        scanner.close();
    }

    private static void basketballWordle(Scanner scanner) {
        String answer = "BASKET";
        System.out.println("\nGuess this 6-letter word: _ A _ K _ T (Hint: Sport)");
        System.out.print("Your guess: ");
        String guess = scanner.nextLine().toUpperCase();

        if (guess.equals(answer)) {
            System.out.println("Correct! You guessed it!");
        } else {
            System.out.println("Oops! The answer was: " + answer);
        }
    }

    private static void countryTrivia(Scanner scanner) {
        System.out.println("\nGuess the country based on these clues:");
        System.out.println("- Famous for sushi");
        System.out.println("- Mt. Fuji is here");
        System.out.println("- Shinto is practiced");
        System.out.print("Your guess: ");
        String guess = scanner.nextLine().trim();

        if (guess.equalsIgnoreCase("Japan")) {
            System.out.println("Correct! It is Japan.");
        } else {
            System.out.println("Not quite. The answer is Japan.");
        }
    }

    private static void gameTip() {
        System.out.println("\nGame Tip of the Day:");
        System.out.println("Always dodge toward a boss’s back left leg in Souls-like games.");
    }
}
