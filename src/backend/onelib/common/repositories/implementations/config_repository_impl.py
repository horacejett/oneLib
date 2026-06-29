from sqlmodel.ext.asyncio.session import AsyncSession

from onelib.common.models.config import Config
from onelib.common.repositories.implementations.base_repository_impl import BaseRepositoryImpl
from onelib.common.repositories.interfaces.config_repository import ConfigRepository


class ConfigRepositoryImpl(BaseRepositoryImpl[Config, str], ConfigRepository):
    """Shared link repository implementation"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Config)
