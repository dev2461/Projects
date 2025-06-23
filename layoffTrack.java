import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class NucleusBot {
    private static final String[] layoffs = {
        "🔴 TechCorp laid off 120 employees globally today.",
        "⚠️ Layoffs at CloudBase hit 8% of workforce.",
        "💼 StartUpX announces hiring freeze and restructures teams."
    };

    private static final String[] sleepingUpdates = {
        "🌙 Most of Asia is currently asleep. 2.5B people are estimated to be resting.",
        "🛌 It's midnight across Europe. Estimated 700M people sleeping.",
        "😴 North America entering peak sleep hours — 400M people offline."
    };

    private static final String[] interviewQs = {
        "💡 CS Interview Tip: Explain how a HashMap handles collisions.",
        "💻 Coding Q: What's the time complexity of quicksort in the worst case?",
        "📘 Java Q: What's the difference between `==` and `.equals()`?"
    };

    public static void main(String[] args) {
        Timer timer = new Timer();
        Random rand = new Random();

        System.out.println("🤖 NucleusBot is running... (Ctrl+C to stop)");

        // Post every 5 seconds for demonstration (can change to minutes/hours)
        timer.schedule(new TimerTask() {
            int postCount = 0;
            @Override
            public void run() {
                switch (postCount % 3) {
                    case 0 -> System.out.println("\n[Layoff Update] " + layoffs[rand.nextInt(layoffs.length)]);
                    case 1 -> System.out.println("\n[Sleeping World] " + sleepingUpdates[rand.nextInt(sleepingUpdates.length)]);
                    case 2 -> System.out.println("\n[Code Interview] " + interviewQs[rand.nextInt(interviewQs.length)]);
                }
                postCount++;
            }
        }, 0, 5000); // 5 seconds interval (adjustable)
    }
}
