from typing import TYPE_CHECKING

from onelib.services.credentials.service import CredentialService
from onelib.services.factory import ServiceFactory

if TYPE_CHECKING:
    from onelib.services.settings.service import SettingsService


class CredentialServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(CredentialService)

    def create(self, settings_service: 'SettingsService'):
        return CredentialService(settings_service)
