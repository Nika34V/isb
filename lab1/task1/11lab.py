import json

def save_key(file_path, shift):
    """
    Предназначена для сохранения значения параметра shift в JSON-файл по указанному пути.
    :param file_path: Путь к файлу
    :param shift: Значение, которое нужно сохранить в файл
    :return: None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({'shift': shift}, file, ensure_ascii=False, indent=4)

def load_text(file_path):
    """
    Предназначена для чтения текстового содержимого из файла по указанному пути
    :param file_path: Путь к файлу
    :return: Функция возвращает строку
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_text(data, file_path):
    """
    Предназначена для сохранения текстовых данных в файл по указанному пути 
    :param file_path: Путь к файлу
    :param data: Текстовые данные, которые нужно записать в файл
    :return: None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def caesar_cipher(text, shift, encrypt=True):
    """
    Реализует шифр Цезаря для русского алфавита
    :param text: Текст, который нужно зашифровать или расшифровать
    :param shift: Текстовые данные, которые нужно записать в файл
    :param encrypt: Флаг, определяющий режим работы функции
    :return:  возвращает строку
    """
    result = []
    for char in text:
        if 'А' <= char <= 'Я':  
            base = ord('А')
            new_char = chr((ord(char) - base + (shift if encrypt else -shift)) % 32 + base)
        elif 'а' <= char <= 'я': 
            base = ord('а')
            new_char = chr((ord(char) - base + (shift if encrypt else -shift)) % 32 + base)
        else:
            new_char = char  
        result.append(new_char)
    return ''.join(result)

def main():
    
    shift = 3  

    save_key('key.json', shift)

    original_text = load_text('original.txt')

    encrypted_text = caesar_cipher(original_text, shift, encrypt=True)
    save_text(encrypted_text, 'encrypted.txt')

    decrypted_text = caesar_cipher(encrypted_text, shift, encrypt=False)
    save_text(decrypted_text, 'decrypted.txt')

    print(f"Шифрование и расшифрование завершены. Файлы: encrypted.txt, decrypted.txt. Ключ сдвига: {shift}")

if __name__ == "__main__":
    main()
