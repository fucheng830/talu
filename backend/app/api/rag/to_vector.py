from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents.base import Document
import os
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOpenAI
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy


embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")


def create_doc(content: str, meta: dict):
    content_doc = Document(page_content=content, metadata=meta)
    return content_doc

def create_content_index(doc):
    """创建文章的高维向量索引"""
    try:
        metadata = {'user_id': str(doc.user_id), 
                    'doc_id': str(doc.document_id)}
        
        # summary_vector = embeddings_model.embed_query(doc.content)
        summary_doc = create_doc(doc.content, metadata)
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run([summary_doc])
        title = doc.title

        texts = [create_doc(summary, {'user_id':metadata['user_id'],
                                      'doc_id':metadata['doc_id'],
                                      'index_type':'summary',
                                      }), 
                create_doc(title, {'user_id':metadata['user_id'],
                                      'doc_id':metadata['doc_id'],
                                      'index_type':'title',
                                      })]
        
        # # 将文章的向量索引保存到数据库
        db = PGVector.from_documents(
            embedding=embeddings_model,
            documents=texts,
            collection_name='收藏夹',
            connection_string=os.environ['SQLALCHEMY_DATABASE_URL'],
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()


def search(query: str):
    store = PGVector(
        connection_string=os.environ['SQLALCHEMY_DATABASE_URL'], 
        embedding_function=embeddings_model, 
        collection_name='收藏夹',
        distance_strategy=DistanceStrategy.COSINE
    )
    
    docs = {}
    for doc, score in store.similarity_search_with_score(query, k=100):
        if doc.metadata['doc_id'] not in docs:
            if doc.metadata['doc_id'] not in docs:
                docs[doc.metadata['doc_id']] = score

    return docs
    
        

if __name__=='__main__':
    search('Agent是什么')
    # 创建一个Document对象

    # 运行create_content_index函数
    # create_content_index(doc)


    # from langchain_community.document_loaders import WebBaseLoader

    # loader = WebBaseLoader("https://www.toutiao.com/article/7320121943812948491/?log_from=7e41c6da3f806_1704526385650")
    # docs = loader.load()

    # chain = load_summarize_chain(llm, chain_type="stuff")

    # print(chain.run())
