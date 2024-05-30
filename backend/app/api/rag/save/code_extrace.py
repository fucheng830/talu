import os
import uuid
import asyncio
import logging
from typing import List, Dict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import GitLoader

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ChatOpenAI instance
llm = ChatOpenAI(temperature=0, model='deepseek-chat', max_retries=5)

def code_summary():
    """
    Generate a summary for a code snippet.

    :return: A PromptTemplate instance.
    """
    prompt_template = """
    TASK: Create a summary for the following file. Use as few words as possible, while retaining details. Use bullet points.
    {file_content}
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["file_content"]
    )
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain

def load_codebase_knowledge(clone_url: str, repo_path):
    """
    Create a knowledge base from a codebase.

    :param url: The URL of the codebase.
    :return: A list of documents from the codebase.
    """
    
    loader = GitLoader(
        clone_url=clone_url,
        repo_path=repo_path,
    )
    documents = loader.load()
    return documents

async def load_and_vector_codebase(url: str, user_id: str, knowledge_id: str):
    """
    Load a codebase and vectorize it.

    :param url: The URL of the codebase.
    :param user_id: The user ID.
    :param knowledge_id: The knowledge ID.
    """
    import hashlib
    id = hashlib.md5(f"{user_id}/{knowledge_id}/{url}".encode('utf-8')).hexdigest()
    save_path = os.environ.get('SAVE_PATH', '/tmp/git')
    repo_path = os.path.join(save_path, id)
   
    documents = load_codebase_knowledge(clone_url=url, repo_path=repo_path)
    summary_chain = code_summary()
    summarys = await asyncio.gather(*[summary_chain.ainvoke({'file_content': doc.page_content}) for doc in documents], return_exceptions=True)

    # Handle exceptions
    for summary in summarys:
        if isinstance(summary, Exception):
            logger.error(f"Error generating summary: {summary}")
        else:
            logger.info(f"Generated summary: {summary}")
            

if __name__ == '__main__':
    asyncio.run(load_and_vector_codebase('https://github.com/linyiLYi/bilibot.git', 'fucheng', 'bilibot'))