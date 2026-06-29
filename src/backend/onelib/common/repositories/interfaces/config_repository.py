from abc import ABC

from onelib.common.models.config import Config
from onelib.common.repositories.interfaces.base_repository import BaseRepository


class ConfigRepository(BaseRepository[Config, str], ABC):
    """Configure warehouse interfaces"""
    pass
