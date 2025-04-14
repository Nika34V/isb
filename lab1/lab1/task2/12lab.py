import json
from collections import Counter
import file_operations_caesar2 as fo

def analyze_frequency(text)->dict:
    """
    Анализирует частоту появления каждого символа в переданном тексте
    :param text: Текст, который нужно проанализировать
    :return: Возвращает словарь
    """
    freq_counter = Counter(text)
    total_chars = sum(freq_counter.values())
    return {char: count / total_chars for char, count in freq_counter.items()}

def create_mapping(cipher_freq, russian_freq)->dict:
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

def decrypt_text(text, mapping)->str:
    """
    Предназначена для расшифровки текста с использованием заранее созданного сопоставления
    :param text: Строка, представляющая зашифрованный текст, который нужно расшифровать.
    :param mapping: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита.
    :return: Расшифрованный текст
    """
    return ''.join(mapping.get(char, char) for char in text)


def main():
    settings = fo.load_json("settings2.json")

    cipher_text = fo.load_text(settings["cipher_text_path"])
    russian_frequencies = fo.load_json(settings["russian_frequencies_path"])
    
    cipher_frequencies = analyze_frequency(cipher_text)
    
    cipher_frequencies_sorted = dict(
        sorted(
            cipher_frequencies.items(),
            key=lambda item: (-item[1], item[0])  
        )
    )
    
    fo.save_json(cipher_frequencies_sorted, settings["cipher_frequencies_output"])
    
    mapping = create_mapping(cipher_frequencies, russian_frequencies)
    
    decrypted_text = decrypt_text(cipher_text, mapping)
    
    fo.save_json(mapping, settings["mapping_output"])
    fo.save_text(decrypted_text, settings["decrypted_text_output"])
    
    print("Расшифровка завершена. Файлы: decrypted.txt, mapping.json, cipher_frequencies.json")
if __name__ == "__main__":
    main()