from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents.base import Document
import os
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOpenAI
from .pgvector import PGVector
from .retriever import PostgresFullTextSearchRetriever
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.retrievers import EnsembleRetriever
from sqlalchemy.orm import Session


embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")


def create_doc(content: str, meta: dict):
    content_doc = Document(page_content=content, metadata=meta)
    return content_doc


def search(query: str, knowledge_id: str, db: Session, **kwargs):
    # 搜索模式
        # 检索算法：最大边际相关性检索 mnr
        # 语义检索
        # 全文检索
        # 混合检索
        # Self-querying
    
       
        # 结果重排 long-Context Reorder
    # 搜索过滤
        # 引用上限 max_length
        # 相关度阈值 threshold
    # 问题补全
        # 是否补齐 multiQuery,增强检索 is_complete
    # 上下文压缩

    bm25_ratio = kwargs.get('bm25_ratio', 0.5)
    embedding_ratio = kwargs.get('embedding_ratio', 0.5)
    
    embedding_retriever = PGVector(
        connection_string=os.environ['SQLALCHEMY_DATABASE_URL'], 
        embedding_function=embeddings_model, 
        collection_id=knowledge_id,
        distance_strategy=DistanceStrategy.COSINE
    ).as_retriever()
    
  
    bm25_retriever = PostgresFullTextSearchRetriever.from_db(db)
    
    combine_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, embedding_retriever], weights=[bm25_ratio, embedding_ratio]
    )

    docs = combine_retriever.get_relevant_documents(query)
    return docs



 
    

