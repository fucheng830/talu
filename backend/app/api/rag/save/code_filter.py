from typing import List, Dict
from pydantic import BaseModel, Field
import asyncio
import os 

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser



async def filter_relative_node(task: str, file_content: str):
    # 创建提示模板
    prompt_template = """
    # User Input
    ## This is what the user requested
    {task}

    # Your Role
    ## This is your role
    Identify the files needed for the user input. 
    {format_instructions}

    # CodeData 
    ## This is the code data
    {file_content}
    """

    class OutPut(BaseModel):
        isneeded: bool = Field(description="是否需要")


    parser = PydanticOutputParser(pydantic_object=OutPut)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["task"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    

    llm = ChatOpenAI(temperature=0, model='deepseek-chat')
    chain = prompt | llm | parser
    
    for i in range(max_retries):
        try:
            result = await chain.ainvoke({'task':task, 'file_content':file_content})
            return result.isneeded
        except Exception as e:
            print(e)


