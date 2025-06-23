import java.util.Scanner;

public class NucleusTools {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        while (running) {
            System.out.println("\n=== dayCity ===");
            System.out.println("[1] Code Interview Flashcard");
            System.out.println("[2] QR Code Scanner (Stub)");
            System.out.println("[3] Music Loop Simulator");
            System.out.println("[0] Exit");

            System.out.print("Choose a tool: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1 -> flashcard(scanner);
                case 2 -> qrScannerStub();
                case 3 -> musicLoop();
                case 0 -> {
                    System.out.println("Exiting Nucleus Tools...");
                    running = false;
                }
                default -> System.out.println("Invalid option.");
            }
        }
        scanner.close();
    }

    private static void flashcard(Scanner scanner) {
        System.out.println("\nFlashcard: What is a Java interface?");
        System.out.println("Press Enter to reveal the answer...");
        scanner.nextLine();
        System.out.println("Answer: A contract that classes can implement. It defines method signatures but no implementation.");
    }

    private static void qrScannerStub() {
        System.out.println("\n[Simulated] QR Code Scanner");
        System.out.println("Feature coming soon: Simulate scanning a QR code and returning text.");
    }

    private static void musicLoop() {
        System.out.println("\n🎵 Music Loop Simulator 🎵");
        System.out.println("* Beat * Clap * Beat * Clap *");
        System.out.println("(Pretend you’re hearing lo-fi beats to relax/study to)");
    }
}
