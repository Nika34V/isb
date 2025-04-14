import json

def load_text(file_path: str) -> str:
    """
    Предназначена для чтения текстового содержимого из файла по указанному пути
    :param file_path: Путь к файлу
    :return: Функция возвращает строку
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_text(data: str, file_path: str) -> None:
    """
    Предназначена для сохранения текстовых данных в файл по указанному пути 
    :param file_path: Путь к файлу
    :param data: Текстовые данные, которые нужно записать в файл
    :return: None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data: dict, file_path: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
