from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generate_symmetric_key(key_size=256):
    """Генерирует симметричный ключ заданного размера.
    Args:
        key_size (int): Размер ключа в битах (по умолчанию 256)   
    Returns:
        bytes: Сгенерированный случайный ключ
    """
    return os.urandom(key_size // 8)

def encrypt_symmetric(data, key):
    """Шифрует данные с использованием симметричного ключа (AES-CBC с padding ANSIX923).
    Args:
        data (bytes): Данные для шифрования
        key (bytes): Ключ шифрования
    Returns:
        bytes: Зашифрованные данные (IV + ciphertext)
    """
    padder = padding.ANSIX923(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return iv + encryptor.update(padded_data) + encryptor.finalize()

def decrypt_symmetric(encrypted_data, key):
    """Дешифрует данные, зашифрованные с помощью симметричного ключа.
    
    Args:
        encrypted_data (bytes): Зашифрованные данные (IV + ciphertext)
        key (bytes): Ключ шифрования
    Returns:
        bytes: Расшифрованные исходные данные
    Raises:
        ValueError: Если возникает ошибка при удалении padding или дешифровании
    """
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    
    unpadder = padding.ANSIX923(128).unpadder()
    return unpadder.update(decrypted_padded) + unpadder.finalize()