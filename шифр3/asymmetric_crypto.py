from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def generate_asymmetric_keys() -> Tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Генерирует пару асимметричных ключей (приватный и публичный).
    Returns:Tuple[RSAPrivateKey, RSAPublicKey]: Кортеж, содержащий приватный и публичный ключи
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key: RSAPublicKey) -> bytes:
    """
    Сериализует публичный ключ в формат PEM.
    Args:public_key (RSAPublicKey): Публичный ключ для сериализации
    Returns:bytes: Сериализованный публичный ключ в формате PEM
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def serialize_private_key(private_key: RSAPrivateKey) -> bytes:
    """
    Сериализует приватный ключ в формат PEM без шифрования.
    Args:private_key (RSAPrivateKey): Приватный ключ для сериализации
    Returns:bytes: Сериализованный приватный ключ в формате PEM
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

def encrypt_asymmetric(data: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифрует данные с использованием публичного ключа RSA.
    Args:
        data (bytes): Данные для шифрования
        public_key (RSAPublicKey): Публичный ключ для шифрования   
    Returns:bytes: Зашифрованные данные
    """
    return public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_asymmetric(encrypted_data: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Дешифрует данные с использованием приватного ключа RSA.
    Args:
        encrypted_data (bytes): Зашифрованные данные
        private_key (RSAPrivateKey): Приватный ключ для дешифрования    
    Returns: bytes: Расшифрованные данные
    """
    return private_key.decrypt(
        encrypted_data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )