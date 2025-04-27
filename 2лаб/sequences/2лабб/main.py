import json
import sys
from pathlib import Path
from tests.nist_tests import frequency_test, runs_test, longest_run_ones_test


def read_config(config_path="config.json"):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка парсинга конфигурационного файла {config_path}")
    except IOError as e:
        raise IOError(f"Ошибка чтения конфигурационного файла: {str(e)}")


def read_sequence(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {path} не найден")
    except IOError as e:
        raise IOError(f"Ошибка ввода-вывода при чтении файла {path}: {str(e)}")


def run_all_tests(sequence):
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


def save_results(results, filename):
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Ошибка при сохранении результатов в файл {filename}: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Ошибка сериализации результатов: {str(e)}")


def main():
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