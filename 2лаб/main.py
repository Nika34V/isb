import json
from tests.nist_tests import frequency_test, runs_test, longest_run_ones_test


def read_sequence(path):
    with open(path, 'r') as file:
        return file.read().strip()


def run_all_tests(sequence):
    results = [
        frequency_test(sequence),
        runs_test(sequence),
        longest_run_ones_test(sequence)
    ]
    return results


def save_results(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def main():
    sources = {
        "cpp": "sequences/cpp_sequence.txt",
        "java": "sequences/java_sequence.txt"
    }

    for name, path in sources.items():
        sequence = read_sequence(path)
        results = run_all_tests(sequence)
        save_results(results, f"results/{name}_results.json")
        print(f"Результаты тестов для {name.upper()} генератора:")
        for result in results:
            print(result)
        print("\n")


if __name__ == "__main__":
    main()
