import argparse
from file_operations import load_settings, save_file, load_file
from symmetric_crypto import generate_symmetric_key, encrypt_symmetric, decrypt_symmetric
from asymmetric_crypto import (
    generate_asymmetric_keys,
    serialize_public_key,
    serialize_private_key,
    encrypt_asymmetric,
    decrypt_asymmetric
)
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def generate_keys(key_size=None):
    """Генерирует и сохраняет симметричный и асимметричные ключи.
    Args:
        key_size (int, optional): Размер симметричного ключа (128, 192 или 256 бит).
            Запрашивается у пользователя.    
    Returns:
        None  
    Raises:
        ValueError: Если указан неподдерживаемый размер ключа
        Exception: При ошибках генерации или сохранения ключей
    """
    try:
        if key_size is None:
            key_size = int(input("Введите длину ключа AES (128, 192, 256): "))
        if key_size not in [128, 192, 256]:
            raise ValueError("Неподдерживаемый размер ключа")
    except ValueError as e:
        print(f"Ошибка ввода размера ключа: {e}")
        raise

    symmetric_key = generate_symmetric_key(key_size)
    private_key, public_key = generate_asymmetric_keys()

    try:
        save_file('public_key.pem', serialize_public_key(public_key))
        save_file('private_key.pem', serialize_private_key(private_key))
        
        encrypted_sym_key = encrypt_asymmetric(symmetric_key, public_key)
        save_file('symmetric_key.bin', encrypted_sym_key)
        
        print("Ключи успешно сгенерированы и сохранены.")
    except Exception as e:
        print(f"Ошибка при генерации или сохранении ключей: {e}")
        raise

def encrypt_data(input_file='original.txt', output_file='encrypted.bin'):
    """Шифрует файл с использованием сохраненных ключей.
    Args:
        input_file (str, optional): Путь к файлу для шифрования. 
            По умолчанию 'original.txt'.
        output_file (str, optional): Путь для сохранения зашифрованного файла.
            По умолчанию 'encrypted.bin'.  
    Returns:
        None
    Raises:
        Exception: При ошибках загрузки ключей или шифрования
    """
    private_key_bytes = load_file('private_key.pem')
    encrypted_sym_key = load_file('symmetric_key.bin')

    private_key = load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = decrypt_asymmetric(encrypted_sym_key, private_key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_data = encrypt_symmetric(data, symmetric_key)
    save_file(output_file, encrypted_data)
    print(f"Файл {input_file} зашифрован и сохранён как {output_file}.")

def decrypt_data(input_file='encrypted.bin', output_file='decrypted.txt'):
    """Дешифрует файл с использованием сохраненных ключей.
    Args:
        input_file (str, optional): Путь к зашифрованному файлу.
            По умолчанию 'encrypted.bin'.
        output_file (str, optional): Путь для сохранения расшифрованного файла.
            По умолчанию 'decrypted.txt'.    
    Returns:
        None  
    Raises:
        Exception: При ошибках загрузки ключей или дешифрования
    """
    private_key_bytes = load_file('private_key.pem')
    encrypted_sym_key = load_file('symmetric_key.bin')

    private_key = load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = decrypt_asymmetric(encrypted_sym_key, private_key)

    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_symmetric(encrypted_data, symmetric_key)
    
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print(f"Файл {input_file} расшифрован и сохранён как {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Запуск генерации ключей')
    group.add_argument('-enc', '--encryption', help='Запуск шифрования данных')
    group.add_argument('-dec', '--decryption', help='Запуск дешифрования данных')
    parser.add_argument('-k', '--key-size', type=int, choices=[128, 192, 256], 
                       help='Длина ключа AES (128, 192, 256)', default=None)
    parser.add_argument('-i', '--input', help='Входной файл (по умолчанию: original.txt для шифрования, encrypted.bin для дешифрования)')
    parser.add_argument('-o', '--output', help='Выходной файл (по умолчанию: encrypted.bin для шифрования, decrypted.txt для дешифрования)')
    args = parser.parse_args()

    match args:
        case argparse.Namespace(generation=True):
            generate_keys(args.key_size)
        case argparse.Namespace(encryption=True):
            input_file = args.input if args.input else 'original.txt'
            output_file = args.output if args.output else 'encrypted.bin'
            encrypt_data(input_file, output_file)
        case argparse.Namespace(decryption=True):
            input_file = args.input if args.input else 'encrypted.bin'
            output_file = args.output if args.output else 'decrypted.txt'
            decrypt_data(input_file, output_file)