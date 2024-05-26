from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
import hashlib
import uuid

from .auth import get_current_user
from ..schemas import *
from ..models import Knowledge, File as FileModel, FileContent, Document
from ..database import get_db
from .rag import load_document
from ..models import Node, NodeRelationship, EmbeddingStore
from .rag.pgvector import PGVector
from .rag.summary import summary, qa_extract
from .rag.search import search

from langchain_core.documents.base import Document as LangchainDocument
from fastapi import UploadFile, File
import os

from langchain_community.embeddings import OpenAIEmbeddings
from sqlalchemy import text


router = APIRouter()


def create_doc(content: str, meta: dict):
    content_doc = LangchainDocument(page_content=content, metadata=meta)
    return content_doc


@router.post("/add_knowledge")
def add_knowledge(
    knowledge: KnowledgeSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    knowledge_db = Knowledge(
        name=knowledge.name,
        cmetadata={"type": knowledge.type},
        user_id=current_user.get("user_id"),
    )
    # knowledge_db = Node(name=knowledge.name, user_id=current_user.get('user_id'), node_type=knowledge.type)
    db.add(knowledge_db)
    db.commit()
    db.refresh(knowledge_db)
    return {"data": knowledge_db, "status": "Success", "message": "添加成功"}


@router.post("/delete_knowledge")
def delete_knowledge(
    knowledgeParam: KnowledgeDeleteSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    knowledge_db = (
        db.query(Knowledge)
        .filter(
            Knowledge.uuid == knowledgeParam.knowledge_id,
            Knowledge.user_id == current_user.get("user_id"),
        )
        .first()
    )
    # knowledge_db = db.query(Node).filter(Node.node_id == knowledgeParam.knowledge_id, Node.user_id == current_user.get('user_id')).first()
    if knowledge_db:
        db.delete(knowledge_db)
        db.commit()
        return {"status": "Success", "message": "删除成功"}
    else:
        return {"status": "Error", "message": "无法找到指定的知识库"}


@router.post("/get_knowledges")
def get_knowledges(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    Knowledges = (
        db.query(Knowledge).filter_by(user_id=current_user.get("user_id")).all()
    )
    return {"data": Knowledges, "status": "Success"}


@router.post("/list_knowledge_data")
def list_knowledge_data(
    knowledge_id: knowledgeId,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 使用.filter()结合JSONB字段提取操作，注意这里要使用Knowledge作为别名
    from sqlalchemy import text

    knowledge_nodes = (
        db.query(Node)
        .filter_by(knowledge_id=knowledge_id.knowledge_id)
        .all()
    )
    return knowledge_nodes


@router.post("/preview_segment_data")
def preview_segment_data(
    params: segmentPreview,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 使用.filter()结合JSONB字段提取操作，注意这里要使用Knowledge作为别名
    from sqlalchemy import text

    segments = (
        db.query(EmbeddingStore)
        .filter(text(f"cmetadata->>'doc_id' = :doc_id"))
        .params(doc_id=params.node_id)
        .all()
    )
    return [{"document": r.document, "cmetadata": r.cmetadata} for r in segments]


@router.post("/delete_node")
def delete_node(
    delete_params: deleteParams,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Ensure the calling user has the right to delete the node
    node_to_delete = (
        db.query(Node)
        .filter(
            Node.node_id == delete_params.node_id,
            Node.user_id == current_user["user_id"],
        )
        .first()
    )
    if not node_to_delete:
        raise HTTPException(status_code=404, detail="Node not found")

    # Delete node relationships (both parent and child references)
    db.query(NodeRelationship).filter(
        (NodeRelationship.parent_id == delete_params.node_id)
        | (NodeRelationship.child_id == delete_params.node_id)
    ).delete(synchronize_session=False)

    # Delete from langchain_pg_embedding where cmetadata->>'doc_id' matches the node_id
    db.query(EmbeddingStore).filter(text("cmetadata->>'doc_id' = :node_id")).params(
        node_id=str(delete_params.node_id)
    ).delete(synchronize_session=False)

    # Now, delete the node itself
    db.delete(node_to_delete)

    db.commit()
    return {"message": "Node and its relationships were successfully deleted."}


@router.post("/upload_file")
def add_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传文件"""
    # 读取file内容
    file_content = file.file.read()
    file_type = file.filename.split(".")[-1]
    # 转为hash
    id = hashlib.sha256(file_content).hexdigest()
    # 查询是否已经存在
    file_record = db.query(FileContent).filter_by(id=id).first()
    if not file_record:
        # 插入文件内容
        new_file_content = FileContent(id=id, file_data=file_content)
        db.add(new_file_content)

    new_file = FileModel(
        cloud_storage_identifier=id,
        file_name=file.filename,
        file_type=file_type,
        file_size=len(file_content),
        user_id=current_user.get("user_id"),
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return {
        "message": "File uploaded successfully",
        "status": "Success",
        "data": new_file,
    }


@router.post("/load_file")
def load_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """读取文件内容"""
    # 保存上传的文件到用户id的本地路径下，没有则创建文件夹，用户id为文件夹名，路径规则为/home/ubuntu/data/user_id

    user_id = current_user.get("user_id")
    save_path = f"/home/ubuntu/data/{user_id}"

    # 创建用户文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 保存文件到用户文件夹
    file_path = os.path.join(save_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    if file.filename.split(".")[-1] in ["docx", "doc"]:
        return load_document.load_word(file_path)
    elif file.filename.split(".")[-1] in ["pdf"]:
        return load_document.load_pdf(file_path)
    elif file.filename.split(".")[-1] in ["xlsx", "xls"]:
        return load_document.load_excel(file_path)
    elif file.filename.split(".")[-1] in ["pptx", "ppt"]:
        return load_document.load_ppt(file_path)
    elif file.filename.split(".")[-1] in ["txt"]:
        return load_document.load_txt(file_path)
    elif file.filename.split(".")[-1] in ["jpg", "jpeg", "png", "gif"]:
        return load_document.load_image(file_path)
    elif file.filename.split(".")[-1] in ["mp4", "avi", "mov", "flv"]:
        return load_document.load_video(file_path)
    elif file.filename.split(".")[-1] in ["mp3", "wav", "flac"]:
        return load_document.load_audio(file_path)
    else:
        return {"message": "File type is not supported.", "status": "Error"}
    # 调用读取文件函数，返回文件的文本内容


@router.post("/split_document")
def load_file(
    doc: SplitHandler,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """切分文档"""
    user_id = current_user.get("user_id")
    import langchain_text_splitters

    splitter = getattr(langchain_text_splitters, doc.handler_name)
    text_splitter = splitter(**doc.params)
    doc_text = [r["content"] for r in doc.documents]
    metadatas = [{"file_name": r["name"]} for r in doc.documents]
    splited_texts = text_splitter.create_documents(doc_text, metadatas)
    return {
        "splited_texts": splited_texts,
        "metadata": {
            "total_segment": len(splited_texts),
            "total_length": len("".join(doc_text)),
        },
    }


@router.post("/extract_document")
def extract_document(
    doc: SplitHandler,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """文档抽取"""
    user_id = current_user.get("user_id")
    docs = []
    if doc.handler_name == "summary":
        # 对文本进行摘要抽取, 返回摘要，摘要的长度由params决定
        for document in doc.documents:
            docs.append(
                {"file_name": document["name"], "summary": summary(document["content"])}
            )
        return docs
    elif doc.handler_name == "qa":
        # 对文本进行问答抽取，返回问题和答案
        for document in doc.documents:
            docs.append(
                {"file_name": document["name"], "qa": qa_extract(document["content"])}
            )
        return docs


@router.post("/upload_data")
def upload_file_data(
    doc: uploadDatas,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """接收上传数据
    doc:

    """
    from langchain_core.documents.base import Document as LangchainDocument
    from sqlalchemy import text
    user_id = current_user.get("user_id")
    texts = []
    for document in doc.data:
        # 插入文件内容
        if document.get("node_id"):
            print("node_id", document["node_id"])
            # 如果存在node_id，则更新内容
            new_container = db.query(Node).filter(Node.node_id == document["node_id"]).first()
            new_container.content = document["content"]
            
            # 删除原有向量索引
            db.query(EmbeddingStore).filter(
                text("cmetadata->>'doc_id' = :node_id")
            ).params(node_id=str(document["node_id"])).delete()
            db.commit()

        else:
            new_container = Node(
                name=document["name"],
                node_type=document["type"],
                description=document.get("summary"),
                data={},
                knowledge_id=doc.knowledge_id, 
                content=document["content"],
                user_id=user_id,
            )

            db.add(new_container)
            db.commit()
            db.refresh(new_container)
        # 插入向量索引

        texts.append(
            LangchainDocument(
                page_content=f"{new_container.name} 是 {new_container.node_type}: {new_container.description}",
                metadata={
                    "user_id": user_id,
                    "doc_id": str(new_container.node_id),
                    "index_type": "summary",
                },
            )
        )

        for i, text in enumerate(document["content_split"]):
            texts.append(
                LangchainDocument(
                    page_content=text,
                    metadata={
                        "user_id": user_id,
                        "doc_id": str(new_container.node_id),
                        "index_type": "content",
                        "index_id": i,
                    },
                )
            )
        if document.get("qa"):
            for qa in document['qa'].get('qa_list'):
                texts.append(
                    LangchainDocument(
                        page_content=qa["question"],
                        metadata={
                            "user_id": user_id,
                            "doc_id": str(new_container.node_id),
                            "index_type": "qa",
                            "answer": qa["answer"],
                        },
                    )
                )

    embeddings_model = OpenAIEmbeddings()
    PGVector.from_documents(
        connection_string=os.environ["SQLALCHEMY_DATABASE_URL"],
        collection_id=doc.knowledge_id,
        embedding=embeddings_model,
        documents=texts,
    )
    return {"status": "Success", "message": "Document created successfully"}


@router.post("/add_content")
def add_content(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """接收在线编辑器的内容"""

    new_container = Node(
        name=document_data.doc_name,
        node_type="datasetTxt",
        description="",
        knowledge_id=document_data.knowledge_id,
        data={
        },
        content=document_data.doc_content,
        user_id=current_user["user_id"],
    )

    db.add(new_container)
    db.commit()
    db.refresh(new_container)

    return {
        "message": "File content has been uploaded successfully.",
        "status": "Success",
        "data": new_container,
    }


@router.post("/add_manual_document")
def add_message(
    document_content: ManualDocumentContent,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """添加数据进入向量索引表"""
    embeddings_model = OpenAIEmbeddings()
    meta = {
        "user_id": current_user["user_id"],
        "doc_id": document_content.node_id,
        "answer": document_content.answer if document_content.answer else "",
        "index_type": "qa",
    }
    texts = create_doc(document_content.question, meta)
    PGVector.from_documents(
        connection_string=os.environ["SQLALCHEMY_DATABASE_URL"],
        collection_id=document_content.knowledge_id,
        embedding=embeddings_model,
        documents=[texts],
    )
    return {"status": "Success", "message": "Document created successfully"}


@router.post("/add_manual_container")
def add_manual_container(
    params: ManulDocument,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a manual container for input."""
    # Create a new container in the database
    new_container = Node(
        name=params.name,
        node_type="datasetManual",
        data={"knowledge_id": params.knowledge_id},
        knowledge_id=params.knowledge_id,
        user_id=current_user.get("user_id"),
    )

    db.add(new_container)
    db.commit()
    db.refresh(new_container)
    return {"status": "Success", "message": "Manual container created successfully"}


@router.post("/get_node_data")
def get_node_data(
    params: GetNodeDataParams,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取节点的数据"""
    record = db.query(Node).filter(Node.node_id == params.node_id).first()
    if record:
        return record
    else:
        raise HTTPException(status_code=404, detail="Node not found")

def get_content_from_url(url):
    import requests
    res = requests.post("https://static.123qiming.com/web_browse/get_content", json={"url": url})
    return res.json()

@router.post("/add_url_content")
async def add_url_content(link: AddUrlContentParams, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """请求参数：
        url: 用户要保存的网页url
    """
    content = get_content_from_url(link.url)
    if not content:
        raise HTTPException(status_code=400, detail="Failed to fetch content from the given URL")
    else:
        new_container = Node(
        name=content['title'],
        node_type="datasetLink",
        description=content['description'],
        knowledge_id=link.knowledge_id,
        data={'source': link.url},
        content=content['markdown'],
        user_id=current_user["user_id"],
    )

    db.add(new_container)
    db.commit()
    db.refresh(new_container)
    
    return new_container


@router.post("/search_node")
async def search_node(params: SearchNodeParams, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """知识库搜索
    """
    
    search_results = search(params.query, params.knowledge_id, db, **params.search_config)
    return search_results


@router.post("/create_code_knowledge")
async def create_code_knowledge(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """创建代码知识库
    """
    
    return 'success'



    

 
