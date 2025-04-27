import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

/**
 * Генерирует случайную бинарную последовательность и сохраняет её в файл.
 *
 * <p>Класс демонстрирует основы работы с файловым вводом-выводом и
 * генерацией случайных чисел в Java.
 *
 * <p>Результат записывается в файл {@code java_sequence.txt}
 * в директорию {@code ../sequences/}.
 *
 * @author Veronika
 * @version 1.0
 * @since 1.0
 */
public class JavaGenerator {

    /**
     * Точка входа в программу.
     *
     * <p>Генерирует 128 случайных битов (0 или 1) и записывает их в файл.
     * Использует {@link java.util.Random} для генерации битов и
     * {@link java.io.FileWriter} для записи в файл.
     *
     * @param args аргументы командной строки (в данной реализации не используются)
     */
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
