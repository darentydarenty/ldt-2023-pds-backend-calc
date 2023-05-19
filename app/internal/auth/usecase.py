from .repository import AuthRepository
from .models import AuthHeadersModel, AuthServiceModel

from app.pkg.connectors.postgresql import NoResultsException
from app.pkg.connectors.http_client import make_signature


class AuthUseCase:
    __auth_repository: AuthRepository

    def __init__(self, auth_repo: AuthRepository):
        self.__auth_repository = auth_repo

    async def validate_service(self, auth_headers: AuthHeadersModel, body: dict) -> bool:
        service: AuthServiceModel
        try:
            service = await self.__auth_repository.get_service_by_public_key(auth_headers.public_key)
        except NoResultsException:
            return False

        if auth_headers.signature == make_signature(
            private_key=service.private_key.get_secret_value(),
            data=body,
        ):
            return True

        return False
