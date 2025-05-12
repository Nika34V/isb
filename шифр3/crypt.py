import argparse
import json
import os
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def save_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def load_file(path):
    with open(path, 'rb') as f:
        return f.read()

def generate_keys(settings_path):
    with open(settings_path) as f:
        paths = json.load(f)

    key_size = int(input("Введите длину ключа AES (128, 192, 256): "))
    if key_size not in [128, 192, 256]:
        raise ValueError("Неподдерживаемый размер ключа")
    symmetric_key = os.urandom(key_size // 8)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    save_file(paths['public_key'], public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo))

    save_file(paths['secret_key'], private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()))

    encrypted_sym_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))

    save_file(paths['symmetric_key'], encrypted_sym_key)
    print("Ключи успешно сгенерированы и сохранены.")

def encrypt_data(settings_path):
    with open(settings_path) as f:
        paths = json.load(f)

    private_key_bytes = load_file(paths['secret_key'])
    encrypted_sym_key = load_file(paths['symmetric_key'])

    private_key = load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = private_key.decrypt(
        encrypted_sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))

    with open(paths['initial_file'], 'rb') as f:
        data = f.read()

    padder = padding.ANSIX923(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(padded_data) + encryptor.finalize()

    save_file(paths['encrypted_file'], encrypted_data)
    print("Файл зашифрован и сохранён.")

def decrypt_data(settings_path):
    with open(settings_path) as f:
        paths = json.load(f)

    private_key_bytes = load_file(paths['secret_key'])
    encrypted_sym_key = load_file(paths['symmetric_key'])

    private_key = load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = private_key.decrypt(
        encrypted_sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))

    with open(paths['encrypted_file'], 'rb') as f:
        encrypted_data = f.read()

    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    with open(paths['decrypted_file'], 'wb') as f:
        f.write(decrypted_data)

    print("Файл успешно расшифрован.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Запуск генерации ключей')
    group.add_argument('-enc', '--encryption', help='Запуск шифрования данных')
    group.add_argument('-dec', '--decryption', help='Запуск дешифрования данных')
    parser.add_argument('-s', '--settings', required=True, help='Путь к settings.json')
    args = parser.parse_args()

    if args.generation:
        generate_keys(args.settings)
    elif args.encryption:
        encrypt_data(args.settings)
    elif args.decryption:
        decrypt_data(args.settings)
