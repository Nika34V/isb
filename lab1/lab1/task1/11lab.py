import sys
from pathlib import Path

import file_operations_caesar as fo

def caesar_cipher(text: str, shift: int, encrypt: bool = True) -> str:
    """
    Реализует шифр Цезаря для русского алфавита
    :param text: Текст, который нужно зашифровать или расшифровать
    :param shift: Текстовые данные, которые нужно записать в файл
    :param encrypt: Флаг, определяющий режим работы функции
    :return:  возвращает строку
    """
    result = []
    for char in text:
        match char:
            case char if 'А' <= char <= 'Я': 
                base = ord('А')
                new_char = chr((ord(char) - base + (shift if encrypt else -shift)) % 32 + base)
            case char if 'а' <= char <= 'я':  
                base = ord('а')
                new_char = chr((ord(char) - base + (shift if encrypt else -shift)) % 32 + base)
            case _:  
                new_char = char
        result.append(new_char)
    return ''.join(result)

def main():
    settings = fo.load_json("settings.json")
    shift = settings["shift"]
    
    fo.save_json({"shift": shift}, settings["key_file"])
    
    original_text = fo.load_text(settings["original_text_file"])
    encrypted_text = caesar_cipher(original_text, shift, encrypt=True)
    fo.save_text(encrypted_text, settings["encrypted_text_file"])
    
    decrypted_text = caesar_cipher(encrypted_text, shift, encrypt=False)
    fo.save_text(decrypted_text, settings["decrypted_text_file"])
    
    print("Шифрование и расшифрование завершены. Файлы:",
          settings["encrypted_text_file"], settings["decrypted_text_file"], "Ключ сдвига:", shift)

if __name__ == "__main__":
    main()
