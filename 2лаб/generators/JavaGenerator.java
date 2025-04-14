import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class JavaGenerator {
    public static void main(String[] args) {
        try {
            FileWriter writer = new FileWriter("../sequences/java_sequence.txt");
            Random rand = new Random();

            for (int i = 0; i < 128; i++) {
                writer.write(rand.nextBoolean() ? "1" : "0");
            }

            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
