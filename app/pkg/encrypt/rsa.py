from .base import BaseEncryptor
from .error import InvalidPublicKey, InvalidPrivateKey

from typing import Optional

from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes


class Rsa(BaseEncryptor):
    def __init__(
        self,
        public_key: Optional[rsa.RSAPublicKey] = None,
        private_key: Optional[rsa.RSAPrivateKey] = None,
    ):
        self.__public_key = public_key
        self.__private_key = private_key

    def encrypt(self, text: str) -> str:
        if self.__public_key is not None:
            return str(self.__public_key.encrypt(
                text.encode("utf-8"),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            ))
        raise InvalidPublicKey()

    def decrypt(self, cipher: str) -> str:
        if self.__private_key is not None:
            return str(self.__private_key.decrypt(
                cipher.encode("utf-8"),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            ))
        raise InvalidPrivateKey()