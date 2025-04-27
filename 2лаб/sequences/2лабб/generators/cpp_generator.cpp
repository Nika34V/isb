/**
 * @file generator.cpp
 * @brief Генератор случайных бинарных последовательностей
 */

 #include <fstream>
 #include <random>
 #include <ctime>
 
 /**
  * @brief Главная функция программы
  * 
  * Генерирует последовательность из 128 случайных битов (0 или 1)
  * и записывает её в файл "../sequences/cpp_sequence.txt".
  * 
  * Использует:
  * - Вихрь Мерсенна (std::mt19937) в качестве генератора случайных чисел
  * - Равномерное распределение (std::uniform_int_distribution) для получения 0 или 1
  * - Текущее время в качестве seed для генератора
  * 
  * @return Код завершения программы (0 - успешное выполнение)
  */
 int main() {
     // Открываем файл для записи
     std::ofstream file("../sequences/cpp_sequence.txt");
     
     // Инициализируем генератор случайных чисел с seed из текущего времени
     std::mt19937 gen(static_cast<unsigned int>(time(nullptr)));
     
     // Создаём распределение для получения 0 или 1 с равной вероятностью
     std::uniform_int_distribution<> dis(0, 1);
 
     // Генерируем и записываем 128 случайных битов
     for (int i = 0; i < 128; ++i) {
         file << dis(gen);
     }
 
     // Закрываем файл
     file.close();
     
     return 0;
 }