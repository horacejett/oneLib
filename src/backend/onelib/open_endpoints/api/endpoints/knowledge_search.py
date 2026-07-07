"""
V2 Open API endpoint for knowledge base semantic search.

Provides a standalone search endpoint that performs vector + keyword retrieval
across one or more knowledge bases and returns the top matching chunks.
"""
from typing import List, Optional

from fastapi import APIRouter, Body, Request
from loguru import logger
from pydantic import BaseModel, Field

from onelib.api.v1.schema.chat_schema import UseKnowledgeBaseParam
from onelib.api.services.workstation.workstation import WorkStationService
from onelib.open_endpoints.domain.utils import get_default_operator_async


class KnowledgeSearchRequest(BaseModel):
    """Request schema for knowledge search."""
    query: str = Field(..., description="Search query text")
    knowledge_ids: List[int] = Field(
        default_factory=list,
        description="List of knowledge base IDs to search. If empty, searches personal knowledge base."
    )
    personal_knowledge_enabled: bool = Field(
        default=True,
        description="Whether to include the user's personal knowledge base in search"
    )
    top_k: int = Field(default=10, ge=1, le=100, description="Maximum number of results to return")


class KnowledgeSearchChunk(BaseModel):
    """A single search result chunk."""
    content: str = Field(..., description="The text content of the chunk")
    file_name: str = Field(default="", description="Source file name")
    score: Optional[float] = Field(default=None, description="Relevance score")
    metadata: Optional[dict] = Field(default=None, description="Additional chunk metadata")


class KnowledgeSearchResponse(BaseModel):
    """Response schema for knowledge search."""
    query: str
    results: List[KnowledgeSearchChunk]
    total: int


router = APIRouter(prefix='/knowledge', tags=['OpenAPI', 'Knowledge Search'])


@router.post('/search', response_model=KnowledgeSearchResponse)
async def search_knowledge(
    request: Request,
    body: KnowledgeSearchRequest = Body(...),
):
    """
    Search knowledge bases semantically for content matching the query.

    Uses Milvus vector search + Elasticsearch keyword search with RRF fusion
    to find the most relevant content chunks across specified knowledge bases.

    Returns up to `top_k` matching chunks with their source file information.
    """
    logger.info(
        f"act=knowledge_search query={body.query} kb_ids={body.knowledge_ids} "
        f"top_k={body.top_k} personal={body.personal_knowledge_enabled}"
    )

    login_user = await get_default_operator_async()

    use_kb_param = UseKnowledgeBaseParam(
        personal_knowledge_enabled=body.personal_knowledge_enabled,
        organization_knowledge_ids=body.knowledge_ids,
    )

    # Use the same retrieval pipeline as the workstation chat completions
    chunks, source_docs = await WorkStationService.queryChunksFromDB(
        question=body.query,
        use_knowledge_param=use_kb_param,
        max_token=body.top_k * 2000,  # rough estimate for token limit
        login_user=login_user,
    )

    results: List[KnowledgeSearchChunk] = []
    if source_docs:
        for i, doc in enumerate(source_docs[:body.top_k]):
            file_name = doc.metadata.get('source') or doc.metadata.get('document_name', '')
            score = doc.metadata.get('score', None)
            # Extract metadata without embedding/internal fields
            clean_meta = {
                k: v for k, v in doc.metadata.items()
                if k not in ('vector', 'embedding') and not k.startswith('_')
            }
            results.append(KnowledgeSearchChunk(
                content=doc.page_content.strip(),
                file_name=str(file_name),
                score=score,
                metadata=clean_meta,
            ))

    return KnowledgeSearchResponse(
        query=body.query,
        results=results,
        total=len(results),
    )


__all__ = ['router']
