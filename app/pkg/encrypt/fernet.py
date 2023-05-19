import base64

from .base import BaseEncryptor
from .error import InvalidFernetKey

from cryptography.fernet import Fernet


class FernetEncryptor(BaseEncryptor):
    __key: Fernet

    def __init__(self, key: str):
        self.__key = Fernet(key=key)

    def encrypt(self, text: str) -> str:
        return str(self.__key.encrypt(text.encode("utf-8")))

    def decrypt(self, cipher: str) -> str:
        return str(self.__key.decrypt(cipher))
