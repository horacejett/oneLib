from abc import ABC

from onelib.common.repositories.interfaces.base_repository import BaseRepository
from onelib.knowledge.domain.models.knowledge import Knowledge


class KnowledgeRepository(BaseRepository[Knowledge, int], ABC):
    """Knowledge Base Repository Interface"""
    pass
