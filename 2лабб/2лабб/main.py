import sys
from typing import Dict, List, Any
from file_operations import read_config, read_sequence, save_results
from tests.nist_tests import frequency_test, runs_test, longest_run_ones_test


def run_all_tests(sequence: str) -> List[Dict[str, Any]]:
    """Запускает все NIST тесты для бинарной последовательности.
    Args:sequence (str): Бинарная последовательность для тестирования.
    Returns: List[Dict[str, Any]]: Список словарей с результатами тестов.
    Raises:
        ValueError: Если последовательность пустая.
        RuntimeError: Если произошла ошибка при выполнении тестов.
    """
    if not sequence:
        raise ValueError("Пустая последовательность для тестирования")
    
    try:
        return [
            frequency_test(sequence),
            runs_test(sequence),
            longest_run_ones_test(sequence)
        ]
    except Exception as e:
        raise RuntimeError(f"Ошибка при выполнении тестов: {str(e)}")


def main() -> None:
    try:
        config = read_config()
        sources = config.get("sources", {})
        
        if not sources:
            raise ValueError("В конфигурационном файле отсутствуют источники данных")

        for name, path in sources.items():
            try:
                print(f"Обработка {name.upper()} генератора...")
                
                sequence = read_sequence(path)
                results = run_all_tests(sequence)
                save_results(results, f"results/{name}_results.json")
                
                print(f"Результаты тестов для {name.upper()} генератора:")
                for result in results:
                    print(result)
                print("\n")
                
            except Exception as e:
                print(f"Ошибка при обработке {name}: {str(e)}", file=sys.stderr)
                continue

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем", file=sys.stderr)
        sys.exit(1)