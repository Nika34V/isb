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

def read_file_with_handling(file_path: str) -> bytes:
    """Читает содержимое файла в бинарном режиме с обработкой возможных ошибок.
    Args:file_path (str): Путь к файлу, который нужно прочитать.  
    Returns:bytes: Содержимое файла в виде байтовой строки. 
    Raises:
        FileNotFoundError: Если указанный файл не существует.
        IOError: Если произошла ошибка ввода/вывода при чтении файла.
        Exception: Если произошла неизвестная ошибка при чтении файла.
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        raise
    except IOError as e:
        print(f"Ошибка ввода/вывода при чтении {file_path}: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка при чтении {file_path}: {e}")
        raise

def generate_keys(key_size: int = 256, 
                 pub_key_path: str = 'public_key.pem',
                 priv_key_path: str = 'private_key.pem',
                 sym_key_path: str = 'symmetric_key.bin'):
    """Генерирует и сохраняет асимметричные ключи и симметричный ключ, зашифрованный открытым ключом.
    Args:
        key_size (int, optional): Размер генерируемого симметричного ключа в битах. По умолчанию 256.
        pub_key_path (str, optional): Путь для сохранения открытого ключа. По умолчанию 'public_key.pem'.
        priv_key_path (str, optional): Путь для сохранения закрытого ключа. По умолчанию 'private_key.pem'.
        sym_key_path (str, optional): Путь для сохранения зашифрованного симметричного ключа. По умолчанию 'symmetric_key.bin'.
    Returns: None
    Raises: Exception: Если произошла ошибка при генерации или сохранении ключей.
    """
    try:
        symmetric_key = generate_symmetric_key(key_size)
        private_key, public_key = generate_asymmetric_keys()

        save_file(pub_key_path, serialize_public_key(public_key))
        save_file(priv_key_path, serialize_private_key(private_key))
        save_file(sym_key_path, encrypt_asymmetric(symmetric_key, public_key))

        print(f"Ключи сохранены:\n- {pub_key_path}\n- {priv_key_path}\n- {sym_key_path}")
    except Exception as e:
        print(f"Ошибка генерации ключей: {e}")
        raise

def encrypt_data(input_file: str = 'original.txt',
                output_file: str = 'encrypted.bin',
                private_key_path: str = 'private_key.pem',
                symmetric_key_path: str = 'symmetric_key.bin'):
    """Шифрует данные из файла с использованием симметричного ключа, который предварительно расшифровывается закрытым ключом.
    Args:
        input_file (str, optional): Путь к исходному файлу для шифрования. По умолчанию 'original.txt'.
        output_file (str, optional): Путь для сохранения зашифрованных данных. По умолчанию 'encrypted.bin'.
        private_key_path (str, optional): Путь к файлу с закрытым ключом. По умолчанию 'private_key.pem'.
        symmetric_key_path (str, optional): Путь к файлу с зашифрованным симметричным ключом. По умолчанию 'symmetric_key.bin'.
    Returns: None
    Raises:
        Exception: Если произошла ошибка в процессе:
            - загрузки ключей
            - расшифровки симметричного ключа
            - чтения исходного файла
            - шифрования данных
            - сохранения результата
    """
    try:
        private_key = load_pem_private_key(load_file(private_key_path), password=None)
        symmetric_key = decrypt_asymmetric(load_file(symmetric_key_path), private_key)
        data = read_file_with_handling(input_file)
        save_file(output_file, encrypt_symmetric(data, symmetric_key))
        print(f"Файл {input_file} -> {output_file}")
    except Exception as e:
        print(f"Ошибка шифрования: {e}")
        raise

def decrypt_data(input_file: str = 'encrypted.bin',
                output_file: str = 'decrypted.txt',
                private_key_path: str = 'private_key.pem',
                symmetric_key_path: str = 'symmetric_key.bin'):
    """Дешифрует данные из файла с использованием симметричного ключа, который предварительно расшифровывается закрытым ключом.
    Args:
        input_file (str, optional): Путь к зашифрованному файлу. По умолчанию 'encrypted.bin'.
        output_file (str, optional): Путь для сохранения расшифрованных данных. По умолчанию 'decrypted.txt'.
        private_key_path (str, optional): Путь к файлу с закрытым ключом. По умолчанию 'private_key.pem'.
        symmetric_key_path (str, optional): Путь к файлу с зашифрованным симметричным ключом. По умолчанию 'symmetric_key.bin'.
    Returns:None
    Raises:
        FileNotFoundError: Если один из указанных файлов не найден
        ValueError: Если возникла проблема с форматом ключей или данных
        Exception: Если произошла другая ошибка в процессе дешифрования
    """
    try:
        private_key = load_pem_private_key(load_file(private_key_path), password=None)
        symmetric_key = decrypt_asymmetric(load_file(symmetric_key_path), private_key)
        encrypted_data = read_file_with_handling(input_file)
        save_file(output_file, decrypt_symmetric(encrypted_data, symmetric_key))
        print(f"Файл {input_file} -> {output_file}")
    except Exception as e:
        print(f"Ошибка дешифрования: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encrypt', action='store_true', help='Шифрование файла')
    group.add_argument('-dec', '--decrypt', action='store_true', help='Дешифрование файла')
    
    parser.add_argument('-k', '--key-size', type=int, choices=[128, 192, 256], 
                       default=256, help='Размер AES ключа (по умолчанию: 256)')
    parser.add_argument('-i', '--input', help='Входной файл')
    parser.add_argument('-o', '--output', help='Выходной файл')
    parser.add_argument('-pub', '--public-key', help='Путь к публичному ключу')
    parser.add_argument('-priv', '--private-key', help='Путь к приватному ключу')
    parser.add_argument('-sym', '--symmetric-key', help='Путь к симметричному ключу')
    
    args = parser.parse_args()
    
    try:
        if args.generate:
            generate_keys(
                key_size=args.key_size,
                pub_key_path=args.public_key or 'public_key.pem',
                priv_key_path=args.private_key or 'private_key.pem',
                sym_key_path=args.symmetric_key or 'symmetric_key.bin'
            )
        elif args.encrypt:
            encrypt_data(
                input_file=args.input or 'original.txt',
                output_file=args.output or 'encrypted.bin',
                private_key_path=args.private_key or 'private_key.pem',
                symmetric_key_path=args.symmetric_key or 'symmetric_key.bin'
            )
        elif args.decrypt:
            decrypt_data(
                input_file=args.input or 'encrypted.bin',
                output_file=args.output or 'decrypted.txt',
                private_key_path=args.private_key or 'private_key.pem',
                symmetric_key_path=args.symmetric_key or 'symmetric_key.bin'
            )
    except Exception as e:
        print(f"Программа завершена с ошибкой: {e}")