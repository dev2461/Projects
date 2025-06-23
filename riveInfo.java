import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.util.Scanner;

public class RiverCrawler {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter river name to search: ");
        String river = scanner.nextLine();

        try {
            // For demo purposes, let's crawl Wikipedia
            String url = "https://en.wikipedia.org/wiki/" + river.replace(" ", "_");
            Document doc = Jsoup.connect(url).get();

            System.out.println("\n🌊 Extracting river info from: " + url + "\n");

            Elements paragraphs = doc.select("p");
            int count = 0;
            for (Element p : paragraphs) {
                String text = p.text();
                if (text.toLowerCase().contains("river")) {
                    System.out.println("• " + text + "\n");
                    count++;
                    if (count >= 5) break; // limit output
                }
            }

            if (count == 0) {
                System.out.println("No relevant river content found.");
            }

        } catch (IOException e) {
            System.out.println("❌ Error fetching or parsing the page.");
            e.printStackTrace();
        }

        scanner.close();
    }
}
