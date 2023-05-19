from abc import abstractmethod


class BaseEncryptor:
    @abstractmethod
    def encrypt(self, text: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, cipher: str) -> str:
        raise NotImplementedError()
