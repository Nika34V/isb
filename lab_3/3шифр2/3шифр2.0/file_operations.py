import json
import os
from typing import Any, Dict, Union, NoReturn

def save_file(path: str, data: bytes) -> None:
    """
    Сохраняет бинарные данные в файл по указанному пути.
    Args:
        path (str): Путь к файлу для сохранения
        data (bytes): Бинарные данные для записи
    Raises:
        IOError: При ошибках ввода/вывода
        Exception: При других неожиданных ошибках
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except IOError as e:
        print(f"Ошибка при сохранении файла {path}: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка при сохранении файла {path}: {e}")
        raise

def load_file(path: str) -> bytes:
    """
    Загружает бинарные данные из файла.
    Args:
        path (str): Путь к файлу для чтения
    Returns:
        bytes: Загруженные бинарные данные
    Raises:
        FileNotFoundError: Если файл не существует
        IOError: При ошибках чтения файла
        Exception: При других неожиданных ошибках
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        raise
    except IOError as e:
        print(f"Ошибка при чтении файла {path}: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла {path}: {e}")
        raise

def load_settings(settings_path: str) -> Dict[str, Any]:
    """
    Загружает настройки из JSON-файла.
    Args:
        settings_path (str): Путь к JSON-файлу с настройками
    Returns:
        Dict[str, Any]: Словарь с загруженными настройками
    Raises:
        FileNotFoundError: Если файл не существует
        json.JSONDecodeError: При ошибках парсинга JSON
        IOError: При ошибках чтения файла
        Exception: При других неожиданных ошибках
    """
    try:
        with open(settings_path) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Ошибка формата JSON в файле настроек: {e}")
                raise
            except Exception as e:
                print(f"Ошибка при загрузке JSON из файла настроек: {e}")
                raise
    except FileNotFoundError:
        print(f"Файл настроек не найден: {settings_path}")
        raise
    except IOError as e:
        print(f"Ошибка при чтении файла настроек: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка при работе с файлом настроек: {e}")
        raise