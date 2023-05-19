from pydantic import BaseModel, PositiveInt, SecretStr


class AuthHeadersModel(BaseModel):
    public_key: str
    signature: str


class AuthServiceModel(BaseModel):
    id: PositiveInt
    name: str
    public_key: str
    private_key: SecretStr
    url: str
