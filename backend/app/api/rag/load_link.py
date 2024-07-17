import os

from langchain_core.documents.base import Document as LangchainDocument
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from ...models import Node
from .parser import split_markdown_text
from .pgvector import PGVector


# 对于网页的向量化
embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="deepseek-chat", temperature=0)


def load_link(url: str):
    # 获取网页的向量化
    try:
        # 获取网页的向量化
        # 这里是一个模拟的函数
        return [random.random() for _ in range(100)]
    except Exception as e:
        # 如果出现异常，返回None
        return None


def structured_content(document: dict):
    # markdown_text = llm_construct_markdown_text(document["content"])

    # document['content'] = markdown_text
    document['summary'] = llm_summary(document["content"])
    document['splited_content'] = split_markdown_text(document['content'])

    return document

def llm_summary(text: str):
    prompt = """
    {text}

    请对以上内容进行总结""".format(text=text)
    
    result = llm.invoke(prompt)
    return result.content

def llm_construct_markdown_text(text):
    prompt = """
    {text}

    以上是一篇mardown书写的文章，请使用更加清晰的层次结构，#,##,###,来分割原文，但是不要动原文的内容，只调整层次结构，并且只返回markdown部分，不需要```markdown```标记。
    """.format(text=text)
    result = llm.invoke(prompt)
    return result.content

def insert_document(document, knowledge_id, user_id, db, **kwargs):
    """
    Insert a document into the database.
    Args:
        document: The document to be inserted.
            dict with keys:
                title: The title of the document.
                summary: The summary of the document.
                content: The content of the document.
                url: The url of the document.
                splited_content: The splited content of the document.
        knowledge_id: The knowledge id of the document.
        user_id: The user id of the document.
        db: The database session.
    """
    document = structured_content(document)
    kwargs['source'] = document['url']
    new_container = Node(
        name=document['title'],
        node_type="datasetLink",
        description=document['summary'],
        knowledge_id=knowledge_id,
        data=kwargs,
        content=document['content'],
        user_id=user_id
    )

    db.add(new_container)
    db.commit()
    db.refresh(new_container)

    # 正文分段向量化
    splited_text = document['splited_content']

    for i, r in enumerate(splited_text):
        splited_text[i].metadata = {
            "user_id": user_id,
            "doc_id": str(new_container.node_id),
            "index_type": "content",
            "index_id": i,
        }
    
    # 总结向量化
    summary = document['summary']

    metadata = {
        "user_id": user_id,
        "doc_id": str(new_container.node_id),
        "index_type": "summary",
    }

    splited_text.append(LangchainDocument(page_content=summary, metadata=metadata))

    # 标题向量化
    title = document['title']
    metadata = {
        "user_id": user_id,
        "doc_id": str(new_container.node_id),
        "index_type": "title",
    }
    splited_text.append(LangchainDocument(page_content=title, metadata=metadata))

    # 插入数据库
    PGVector.from_documents(
        connection_string=os.environ["SQLALCHEMY_DATABASE_URL"],
        collection_id=knowledge_id,
        embedding=embeddings_model,
        documents=splited_text,
    )
    return new_container