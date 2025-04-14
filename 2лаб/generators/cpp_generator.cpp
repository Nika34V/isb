#include <fstream>
#include <random>
#include <ctime>

int main() {
    std::ofstream file("../sequences/cpp_sequence.txt");
    std::mt19937 gen(static_cast<unsigned int>(time(nullptr)));
    std::uniform_int_distribution<> dis(0, 1);

    for (int i = 0; i < 128; ++i) {
        file << dis(gen);
    }

    file.close();
    return 0;
}
