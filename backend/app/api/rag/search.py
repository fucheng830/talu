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

def combine_retriever(embeddings_model, knowledge_id, db, **kwargs):
    """
    kwargs:
        bm25_ratio: BM25检索的权重
        embedding_ratio: 语义检索的权重
        search_num: 检索结果数量
        filter: 过滤条件 dict {'index_type': 'summary'}
    """
    
    bm25_ratio = kwargs.get('bm25_ratio', 0.5)
    embedding_ratio = kwargs.get('embedding_ratio', 0.5)

    search_num = kwargs.get('search_num', 20)
    filter = kwargs.get('filter', {'index_type': 'summary'})
    
    embedding_retriever = PGVector(
        connection_string=os.environ['SQLALCHEMY_DATABASE_URL'], 
        embedding_function=embeddings_model, 
        collection_id=knowledge_id,
        distance_strategy=DistanceStrategy.COSINE
    ).as_retriever(search_kwargs={'k': search_num, 'filter': filter})
    
  
    bm25_retriever = PostgresFullTextSearchRetriever.from_db(db, k=search_num)
    
    return EnsembleRetriever(
        retrievers=[bm25_retriever, embedding_retriever], weights=[bm25_ratio, embedding_ratio]
    )



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
    retriever = combine_retriever(embeddings_model, knowledge_id, db, **kwargs)
    docs = retriever.get_relevant_documents(query)
    return docs





 
    

