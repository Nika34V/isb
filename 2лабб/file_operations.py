import json
from pathlib import Path
from typing import Dict, Any, List


def read_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Читает и парсит конфигурационный файл в формате JSON.
    Args:config_path (str): Путь к конфигурационному файлу. По умолчанию "config.json".
    Returns:Dict[str, Any]: Словарь с данными конфигурации.
    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
        ValueError: Если произошла ошибка парсинга JSON.
        IOError: Если произошла ошибка ввода-вывода при чтении файла.
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка парсинга конфигурационного файла {config_path}")
    except IOError as e:
        raise IOError(f"Ошибка чтения конфигурационного файла: {str(e)}")


def read_sequence(path: str) -> str:
    """Читает бинарную последовательность из файла.
    Args:path (str): Путь к файлу с последовательностью.
    Returns: str: Строка с бинарной последовательностью.
    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: Если произошла ошибка ввода-вывода при чтении файла.
    """
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {path} не найден")
    except IOError as e:
        raise IOError(f"Ошибка ввода-вывода при чтении файла {path}: {str(e)}")


def save_results(results: List[Dict[str, Any]], filename: str) -> None:
    """Сохраняет результаты тестов в JSON файл.
    Args:results (List[Dict[str, Any]]): Список результатов для сохранения.
        filename (str): Имя файла для сохранения результатов.
    Returns:None
    Raises:
        IOError: Если произошла ошибка при сохранении файла.
        TypeError: Если результаты не могут быть сериализованы в JSON.
    """
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Ошибка при сохранении результатов в файл {filename}: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Ошибка сериализации результатов: {str(e)}")