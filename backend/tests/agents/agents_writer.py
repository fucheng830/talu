from fastapi import FastAPI, Request, Response, APIRouter
from fastapi import Depends, HTTPException
import json
import requests

import os
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.agents import tool

from langchain.callbacks.base import BaseCallbackHandler
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.agents import Tool
from langchain.agents import AgentExecutor, tool

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.adapters.openai import convert_dict_to_message
from langchain.adapters.openai import convert_message_to_dict
from fastapi.responses import StreamingResponse
from .auth import get_current_user
import re
from .sse_format import sse_json
from sse_starlette.sse import EventSourceResponse

from ..database import get_db
from ..models import Agent
from .agent import load_tools

from langchain.tools.render import format_tool_to_openai_function
from langchain_community.adapters.openai import convert_openai_messages

# Create an APIRouter instance
router = APIRouter()




def chat(current_user, **kwargs):
    """问答入口"""
    from ..application.tools.writer import rewriter
    # gpt-3.5-turbo-1106
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", 
                     temperature=0, 
                     streaming=True
                     )

    dell_e_3 = DallEAPIWrapper()
    dell_e_3.model_name = 'dall-e-3'

    image_generate = Tool(
        "Dall-E-Image-Generator",
        dell_e_3.run,
        "A wrapper around OpenAI DALL-E API. Useful for when you need to generate images from a text description. Input should be an image description.",
    )

    rewriter = Tool(
        "Rewriter",
        rewriter, 
        "A tool to rewrite an article based on the input content.",
    )


    @tool
    def save_content(url: str, user_id: str)-> str:
        """Receive the URL and save the article.
            Args:
                url: str
                user_id: str
        """
        print(user_id)
        try:
            headers = {"Authorization": f"Bearer {current_user['token']}"}
            res = requests.post('http://127.0.0.1:8002/save_content_from_link', json={'url':url}, headers=headers, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                return "保存成功"
            else:
                return '抱歉保存出现问题'
        except Exception as e:
            print(e)
            return '抱歉保存出现问题'

    @tool
    def search_content(text: str)->json:
        """根据用户的数据，搜索数据库中最相关的文章"""
        try:
            headers = {"Authorization": f"Bearer {current_user['token']}"}
            res = requests.post('http://127.0.0.1:8002/search_content', json={'text': text}, headers=headers, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                return res.json()
            else:
                return {'error':'抱歉保存出现问题'}
        except Exception as e:
            print(e)
            return {'error':'抱歉保存出现问题'}
        
    @tool
    def get_content(url: str)->json:
        """通过url获取文章内容"""
        try:
            headers = {"Authorization": f"Bearer {current_user['token']}"}
            res = requests.post('http://127.0.0.1:8002/get_content', json={'url': url}, headers=headers, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                return res.json()
            else:
                return {'error':'抱歉文章读取出现问题'}
        except Exception as e:
            print(e)
            return {'error':'抱歉文章读取出现问题'}
        


    tools = [rewriter, get_content]

# When a user inputs a URL, you should, automatically, save the article to the database.
# You are a user assistant based on a vector library, capable of helping users save articles through URLs, and able to support answering user questions by searching articles in the vector library based on input queries.
# You can also help users generate images based on the description of the image.
# You can also help user rewrite articles based on the URL.
# Example:
#     - When a user directly provides a URL, request the save_content tool to save the article to the database.
#         like     https://mp.weixin.qq.com/s/Imk7UvjtumMNgYp68hnHLg
#     - When a user inputs a keyword, request the search_content tool to search for the most relevant articles in the database.
#         like 请帮我搜索一下Agents相关的文章
    
    system_prompt = """
#Role:你是一个具有链接浏览能力的文章写作助手。
#Task:你的任务是帮助用户写文章。
- 当用户直接提供URL时，自动调用get_content，然后调用rewriter。 
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    from langchain.agents.format_scratchpad import format_to_openai_function_messages
    from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    return agent_executor





@router.post('/v1/chat/completions')
async def chat_process(request: Request, current_user: dict = Depends(get_current_user)):
    """问答入口"""
    import time
    data = await request.json()
    print(data)
    messages = data['messages']
    input_text = messages.pop(-1)['content']
    agent_executor = chat(current_user, **data)
    if data.get('stream'):
        async def stream_chat():
            async for chunk in agent_executor.astream_log(
                {"input": input_text,
                "chat_history": [convert_dict_to_message(message) for message in messages]
                }
                ):
                
                for op in chunk.ops:
                    if op["op"] == "add" and re.match(r"^\/logs\/ChatOpenAI(?::\d+)?\/streamed_output\/\-$", op["path"]):
                        row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                        yield json.dumps(row_data)
                    
            
                # yield json.dumps(sse_json('', finish_reason='stop'))
        return EventSourceResponse(stream_chat(), media_type="text/event-stream")
    else:
        output = agent_executor.invoke(
            {"input": input_text,
            "chat_history": [convert_dict_to_message(message) for message in messages]
            })
        data = {
            "model": "glm3",
            "choices": [
                {
                "index": 0,
                "message": {
                    "content": output['output'],
                    "role": "assistant"
                },
                "finish_reason": None,
                "logprobs": None
                }
            ],
            "created": int(time.time()),
            "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
            "object": "chat.completion",
            "usage": {
                "prompt_tokens": 57,
                "completion_tokens": 17,
                "total_tokens": 74
            }
            }                    
        return data   



def init_agent(config, db):
    """初始化agent"""
    from langchain.agents import create_openai_tools_agent
    from langchain_openai import ChatOpenAI
    model_name = config.llm['model']
    if model_name=='gpt-4-turbo-preview':
        api_key = os.environ.get('OPENAI_API_KEY_PLUS')
    else:
        api_key = os.environ.get('OPENAI_API_KEY')

    print(api_key)
    print(model_name)

    llm = ChatOpenAI(
                     model=config.llm['model'], 
                     temperature=config.llm.get('temperature', 0), 
                     streaming=config.llm.get('streaming', True),
                     api_key=api_key
                     )
    print(llm)
    tools = load_tools(config.tools, db)

    system_prompt = config.system_prompt

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


@router.post('/{agent_id}/v1/chat/completions')
async def app_chat(agent_id:str, request: Request, db: Session = Depends(get_db)):
    """问答入口"""
    data = await request.json()
    agent_config = db.query(Agent).filter_by(id=agent_id).first()
    if not agent_config:
        raise HTTPException(status_code=404, detail="Agent not found")
    data = await request.json()
    messages = data['messages']
    
    if not agent_config.gid:
        input_text = messages.pop(-1)['content']
        agent_executor = init_agent(agent_config, db)
        if data.get('stream'):
            async def stream_chat():
                async for chunk in agent_executor.astream_log(
                    {"input": input_text,
                    "chat_history": [convert_dict_to_message(message) for message in messages]
                    }
                    ):
                    
                    for op in chunk.ops:
                        if op["op"] == "add" and re.match(r"^\/logs\/ChatOpenAI(?::\d+)?\/streamed_output\/\-$", op["path"]):
                            row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                            yield json.dumps(row_data)
                        
                
                    # yield json.dumps(sse_json('', finish_reason='stop'))
            return EventSourceResponse(stream_chat(), media_type="text/event-stream")
        else:
            
            output = agent_executor.invoke(
                {"input": input_text,
                "chat_history": [convert_dict_to_message(message) for message in messages]
                }
                )                    
            return sse_json(output['output'])  

    else:
        # 使用openai的api
        llm = ChatOpenAI(model=agent_config.gid, 
                        streaming=True,
                        api_key=os.environ.get('OPENAI_API_KEY_PLUS')
                     )
        langchain_messages = convert_openai_messages(messages)


        if data.get('stream'):
            async def stream_chat():
                async for chunk in llm.astream_log(
                    langchain_messages
                    ):
                    for op in chunk.ops:
                        if op["op"] == "add" and re.match(r"^\/streamed_output\/\-$", op["path"]):
                            row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                            yield json.dumps(row_data)
                
                    # yield json.dumps(sse_json('', finish_reason='stop'))
            return EventSourceResponse(stream_chat(), media_type="text/event-stream")
        else:
            output = agent_executor.invoke(
               langchain_messages
                )                    
            return sse_json(output['output'])  



@router.post('/{agent_id}/conversation')
async def app_chat(agent_id:str, request: Request, db: Session = Depends(get_db)):
    """问答入口"""
    data = await request.json()
    agent_config = db.query(Agent).filter_by(id=agent_id).first()
    if not agent_config:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    data = await request.json()
    messages = data['messages']

    if not agent_config.gid:
        input_text = messages.pop(-1)['content']
        agent_executor = init_agent(agent_config)
        if data.get('stream'):
            async def stream_chat():
                async for chunk in agent_executor.astream_log(
                    {"input": input_text,
                    "chat_history": [convert_dict_to_message(message) for message in messages]
                    }
                    ):
                    
                    for op in chunk.ops:
                        if op["op"] == "add" and re.match(r"^\/logs\/ChatOpenAI(?::\d+)?\/streamed_output\/\-$", op["path"]):
                            row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                            yield json.dumps(row_data)
                        
                
                    # yield json.dumps(sse_json('', finish_reason='stop'))
            return EventSourceResponse(stream_chat(), media_type="text/event-stream")
        else:
            
            output = agent_executor.invoke(
                {"input": input_text,
                "chat_history": [convert_dict_to_message(message) for message in messages]
                }
                )                    
            return sse_json(output['output'])  

    else:
        # 使用openai的api
        llm = ChatOpenAI(model=agent_config.gid, 
                        streaming=True,
                        api_key='sk-2YIT9ALUSqepiChpF947A14dFb5d4bD89c54B7Fc1e755fBd'
                     )
        langchain_messages = convert_openai_messages(messages)


        if data.get('stream'):
            async def stream_chat():
                async for chunk in llm.astream_log(
                    langchain_messages
                    ):
                    for op in chunk.ops:
                        if op["op"] == "add" and re.match(r"^\/streamed_output\/\-$", op["path"]):
                            row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                            yield json.dumps(row_data)
                
                    # yield json.dumps(sse_json('', finish_reason='stop'))
            return EventSourceResponse(stream_chat(), media_type="text/event-stream")
        else:
            output = agent_executor.invoke(
               langchain_messages
                )                    
            return sse_json(output['output']) 


@router.post('/conversation/gen_title')
async def gen_title(request: Request, db: Session = Depends(get_db)):
    """问答入口"""
    data = await request.json()
    messages = data['messages']
    contents = ['{}: {}'.format(message['role'], message['content']) for message in messages]
    prompt = """
    你是一个bot，你的任务是生成一个标题，这个标题是对以下对话的总结。
    {}
    请按照以下要求返回对话标题。
    1、请直接输出对话标题。
    2、尽量简洁明了。
    3、尽量包含对话的主要内容。
    4、尽量包含对话的亮点。
    5、尽量包含对话的结论。
    6、不要出现标点符号。
    """.format('\n'.join(contents))
    llm = ChatOpenAI(model="gpt-3.5-turbo", 
                     temperature=0, 
                     streaming=False
                     )
    title = llm.predict(prompt)
    return {'status':'Success', 'data':title}





    