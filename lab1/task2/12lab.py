import json
from collections import Counter

def load_cipher_text(file_path):
    """
    Предназначена  для чтения текстового содержимого из файла по указанному пути
    :param file_path: Путь к файлу
    :return: Возвращает строку
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_russian_frequencies(file_path):
    """
    Предназначена  для загрузки данных о частоте использования русских букв
    :param file_path: Путь к файлу
    :return: Возвращает словарь
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def analyze_frequency(text):
    """
    Анализирует частоту появления каждого символа в переданном тексте
    :param text: Текст, который нужно проанализировать
    :return: Возвращает словарь
    """
    freq_counter = Counter(text)
    total_chars = sum(freq_counter.values())
    return {char: count / total_chars for char, count in freq_counter.items()}

def create_mapping(cipher_freq, russian_freq):
    """
    Предназначена для создания сопоставления между символами зашифрованного текста и символами русского алфавита
    :param cipher_freq: Словарь, где ключи — это символы зашифрованного текста, а значения — их частоты
    :param cipher_freq: Словарь, где ключи — это символы русского алфавита, а значения — их частоты
    :return: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита
    """
    sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_russian = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)
    
    mapping = {}
    for (cipher_char, _), (russian_char, _) in zip(sorted_cipher, sorted_russian):
        if cipher_char not in mapping.values():  
            mapping[cipher_char] = russian_char
    return mapping

def decrypt_text(text, mapping):
    """
    Предназначена для расшифровки текста с использованием заранее созданного сопоставления
    :param text: Строка, представляющая зашифрованный текст, который нужно расшифровать.
    :param mapping: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита.
    :return: Расшифрованный текст
    """
    return ''.join(mapping.get(char, char) for char in text)

def save_json(data, file_path):
    """
    предназначена для сохранения данных в формате JSON
    :param data: Данные, которые нужно сохранить
    :param file_path: Путь к файлу
    :return: None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def save_text(data, file_path):
    """
    Предназначена для сохранения текстовых данных в файл
    :param data: Строка, содержащая текстовые данные, которые нужно сохранить в файл
    :param file_path: Путь к фалу
    :return: None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def main():
    cipher_text = load_cipher_text('cipher_text.txt')
    russian_frequencies = load_russian_frequencies('russian_letter_frequency.json')
    
    cipher_frequencies = analyze_frequency(cipher_text)
    
    cipher_frequencies_sorted = dict(
        sorted(
            cipher_frequencies.items(),
            key=lambda item: (-item[1], item[0])  
        )
    )
    
    save_json(cipher_frequencies_sorted, 'cipher_frequencies.json')
    
    mapping = create_mapping(cipher_frequencies, russian_frequencies)
    decrypted_text = decrypt_text(cipher_text, mapping)
    
    save_json(mapping, 'mapping.json')
    save_text(decrypted_text, 'decrypted.txt')
    
    print("Расшифровка завершена. Файлы: decrypted.txt, mapping.json, cipher_frequencies.json")

if __name__ == "__main__":
    main()