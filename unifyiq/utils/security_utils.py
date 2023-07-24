from base64 import b64encode, b64decode

from Crypto.Cipher import AES

from utils.configs import get_storage_encryption_key


class SecurityUtils:
    def __init__(self):
        self.key = get_storage_encryption_key().encode('utf-8')

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        raw = b64decode(encrypted_data)
        nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
