from __future__ import annotations
from typing import List
from sqlalchemy import text
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from sqlalchemy.orm import Session
from typing import Any


class PostgresFullTextSearchRetriever(BaseRetriever):
    """Retriever using PostgreSQL's full text search."""

    db: Session
    k: int = 4

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True


    @classmethod
    def from_db(
        cls,
        db: Session,
        k: int = 4,
        **kwargs: Any,
    ) -> PostgresFullTextSearchRetriever:
        """
        """
        return cls(
            db=db, k=k, **kwargs
        )


    # ... 其他方法 ...

    def _get_relevant_documents(self, query: str, **kwargs) -> List[Document]:
        """
        获取与查询最相关的文档。
        Args:
            query: 查询字符串。
            **kwargs: 其他参数。
        Returns:
            Document列表。
        """
        
        # SQL 查询使用参数化来防止SQL注入
        sql_query = text(
            """SELECT document, cmetadata FROM langchain_pg_embedding
            WHERE to_tsvector('english', document) @@ plainto_tsquery('english', :query) 
            LIMIT :limit"""
        )
        result = self.db.execute(sql_query, {'query': query, 'limit': self.k})
        document_rows = result.fetchall()
      
        
        # 将查询结果转换成Document实例列表
        documents = [Document(page_content=row[0], metadata=row[1]) for row in document_rows]
        return documents


