import java.util.Scanner;

public class NucleusLife {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        while (running) {
            System.out.println("\n=== NeuralLoops ===");
            System.out.println("[1] Baby/Plant Care Log");
            System.out.println("[2] Recipe & Tea Tip");
            System.out.println("[3] Train Map Snapshot");
            System.out.println("[0] Exit");

            System.out.print("Choose a feature: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1 -> careLog(scanner);
                case 2 -> teaTip();
                case 3 -> trainMap();
                case 0 -> {
                    System.out.println("Goodbye from Nucleus Life!");
                    running = false;
                }
                default -> System.out.println("Invalid option.");
            }
        }
        scanner.close();
    }

    private static void careLog(Scanner scanner) {
        System.out.println("\n--- Care Log ---");
        System.out.print("Log for baby or plant? ");
        String target = scanner.nextLine();
        System.out.print("Enter note: ");
        String note = scanner.nextLine();
        System.out.println("Saved: [" + target + "] " + note);
    }

    private static void teaTip() {
        System.out.println("\n🍵 Recipe & Tea Tip 🍵");
        System.out.println("Green tea is best brewed at 80°C to preserve antioxidants.");
    }

    private static void trainMap() {
        System.out.println("\n🚆 Sample Train Route:");
        System.out.println("City Center -> West End -> Airport Express");
        System.out.println("This is a static preview. Map visualization coming in future GUI version.");
    }
}
