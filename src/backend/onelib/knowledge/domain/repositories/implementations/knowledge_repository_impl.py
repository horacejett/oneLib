from typing import Union

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from onelib.common.repositories.implementations.base_repository_impl import BaseRepositoryImpl
from onelib.knowledge.domain.models.knowledge import Knowledge
from onelib.knowledge.domain.repositories.interfaces.knowledge_repository import KnowledgeRepository


class KnowledgeRepositoryImpl(BaseRepositoryImpl[Knowledge, int], KnowledgeRepository):
    """Knowledge Base Repository Implementation Class"""

    def __init__(self, session: Union[AsyncSession, Session]):
        super().__init__(session, Knowledge)
