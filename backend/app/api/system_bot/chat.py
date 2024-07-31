from fastapi import FastAPI, Request, Response, APIRouter
from fastapi import Depends, HTTPException
import json
import requests
import time

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
from ..common.auth import get_current_user
import re
from ..sse_format import sse_json
from sse_starlette.sse import EventSourceResponse

from ...database import get_db, set_key, get_key
from ...models import *
from ..tool import context_tools

from langchain.tools.render import format_tool_to_openai_function
from langchain_community.adapters.openai import convert_openai_messages
from ..agent.load_agent import load_agent

router = APIRouter()

def agent_create_copliot(agent_id, current_user, db):
    """问答入口"""
    context_tools_map = context_tools(db=db, current_user=current_user, agent_id=agent_id)
    generate_profile_pic = context_tools_map['generate_profile_pic']
    update_behavior = context_tools_map['update_behavior']
    tools = [generate_profile_pic, update_behavior]

    system_prompt = """

您好，我们将开始创建一个新的GPT，它就像是一个可以具有额外能力的聊天机器人。每条用户消息都是一个命令，用于处理和更新GPT的行为。当用户告诉我们GPT应该如何行为时，他们指的是我们正在创建的GPT，而不是我们自己。如果没有头像，我们必须调用generate_profile_pic生成一个。如果用户明确要求，我们将生成一个头像，否则不会生成头像。我们将保持作为创建GPT的专家的语气和观点。GPT的个性不应影响我们回应的风格或语气。如果我们向用户提问，我们不会自行回答。我们可以建议答案，但必须让用户确认。GPT也能够参考用户上传的文件来更新行为。

我们将遵循以下步骤：

1. 用户的第一条消息是关于这个GPT应该如何行为的宽泛目标。我们将在gizmo_editor_tool上调用update_behavior，参数包括："context", "description", "prompt_starters"。完成后，继续步骤2。

2. 我们的目标是为GPT确定一个名字。我们会建议一个名字，并要求用户确认。我们必须提供一个建议的名字供用户确认。如果用户明确指定了一个名字，我们就假设它已经被确认了。如果是我们自己生成的名字，我们必须让用户确认。一旦确认，就调用update_behavior并只传入name参数，然后继续步骤3。

3. 我们的目标是为GPT生成一个头像。我们将使用generate_profile_pic生成一个初始头像，然后询问用户是否喜欢并希望进行任何修改。记住，使用generate_profile_pic生成头像无需确认。每次细化后都生成新的头像，直到用户满意为止，然后继续步骤4。

4. 我们现在将引导用户细化上下文。上下文应该包括"角色和目标"、"限制"、"指导原则"、"澄清"和"个性化"等主要领域。我们将引导用户一一定义每个主要领域。我们不会同时提示多个领域。我们每次只会问一个问题。我们的提示应该使用引导性、自然和简单的语言，并且不会提及我们正在定义的领域的名称。例如，"限制"应该被提示为"应该强调或避免什么？"，"个性化"应该被提示为"你希望我如何交谈"。我们的引导问题应该是不言自明的；我们不需要问用户"你怎么看？"。每个提示都应该参考并建立在现有状态之上。每次互动后都调用update_behavior。

在这些步骤中，我们不会提示或确认"description"或"prompt_starters"的值。但是，在更新上下文时，我们仍然会为这些生成值。我们不会提及"步骤"；我们将自然地进行下一步。

**我们必须按顺序完成所有这些步骤。不要跳过任何步骤。**

请用户在旁边的独立聊天对话框中尝试GPT。告诉他们，我们可以听取他们对GPT的任何细化意见。以一个问题结束这条消息，不要说"让我知道！"。

完成上述步骤后，我们现在处于迭代细化模式。用户会提示我们进行更改，我们必须在每次互动后调用update_behavior。在这里，我们可以提出澄清问题。

"""
    llm = ChatOpenAI(model="deepseek-chat", 
                     temperature=0, 
                     streaming=True,
                     api_key=os.environ.get('OPENAI_API_KEY_PLUS')
                     )

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




class ManageContext:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    async def update_tokens(self):
        new_token_count = self.user.user_info.get('usable_token', 0) - 1  # 假设每次对话消耗1个token
        # self.user.user_info['usable_token'] = new_token_count
        # self.db.query(User).filter_by(user_id=self.user.user_id).update({'user_info': self.user.user_info})
        # self.db.commit()
        print('Tokens updated:', new_token_count)


def check_vip_limit(user_id, limit=100):
    """检查vip模型是否可用"""
    dt = datetime.now().strftime('%Y%m%d')
    key = f'plus_{user_id}_{dt}'
    used_num = get_key(key)
    if used_num is None:
        used_num = 0
        used_num +=1
        set_key(key, used_num, ex=60*60*24)
        
    else:
        used_num = int(used_num)
        if used_num<=limit:
            used_num+=1
            set_key(key, used_num, ex=60*60*24)
        else:
            return False
    return True

@router.post('/{agent_id}/v1/chat/{agent_type}')
async def app_chat(agent_id:str, 
                   agent_type:str, 
                   request: Request, 
                   db: Session = Depends(get_db), 
                   current_user: dict = Depends(get_current_user)):
    """问答入口"""
    # 检查用户是否有权限
    user_id = current_user['user_id']
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        if user.vip_end_time is not None and user.vip_end_time<datetime.now():
            raise HTTPException(status_code=401, detail="会员已过期")
        
        elif user.vip_end_time is None:
            usable_token = user.user_info.get('usable_token', 0)
            if usable_token<=0:
                raise HTTPException(status_code=429, detail="您的可用对话次数不足，请订阅会员")
            else:
                user.user_info['usable_token'] -= 1
                db.query(User).filter_by(user_id=user_id).update({'user_info': user.user_info})
                db.commit()

    else:
        raise HTTPException(status_code=401, detail="用户未注册")
    
    # 检查是否已经使用完当日额度
    if not check_vip_limit(user_id):
        raise HTTPException(status_code=429, detail="您的VIP模型使用次数已经用完，请明天再试")
    
    data = await request.json()
    messages = data['messages']

    if agent_type=='agent_create_compilot':
        return chat_with_compilot(agent_id, messages, data, db, user_id)
    else:
        agent_config = db.query(Agent).filter_by(id=agent_id).first()
        if not agent_config:
            raise HTTPException(status_code=404, detail="Agent not found")

        if not agent_config.gid:
            return chat_with_agent(agent_config, messages, data, db, user_id)
        else:
            pass
        
        
def chat_with_compilot(agent_id, messages, data, db, user):
    input_text = messages.pop(-1)['content']
    agent_executor = agent_create_copliot(agent_id, user, db)
    if data.get('stream'):
        async def stream_chat(db, user):
            try:
                async for chunk in agent_executor.astream_log(
                    {"input": input_text,
                    "chat_history": [convert_dict_to_message(message) for message in messages]
                    }
                    ):
                    
                    for op in chunk.ops:
                        if op["op"] == "add":
                            # print(op)
                            if re.match(r"^\/logs\/ChatOpenAI(?::\d+)?\/streamed_output\/\-$", op["path"]):
                                row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                                yield json.dumps(row_data)
      
            finally:
                yield json.dumps(sse_json('', finish_reason='stop'))
  

        return EventSourceResponse(stream_chat(db, user), media_type="text/event-stream")
    else:
        
        output = agent_executor.invoke(
            {"input": input_text,
            "chat_history": [convert_dict_to_message(message) for message in messages]
            }
            )                    
        return sse_json(output['output']) 


def chat_with_agent(agent_config, messages, data, db, user):
    """调用agent"""
    input_text = messages.pop(-1)['content']
    agent_executor = load_agent(agent_config, db)
    if data.get('stream'):
        async def stream_chat(db, user):
            # manage_context = ManageContext(db, user)
            try:
                async for chunk in agent_executor.astream_log(
                    {"input": input_text,
                    "chat_history": [convert_dict_to_message(message) for message in messages]
                    }
                    ):
                    
                    for op in chunk.ops:
                        if op["op"] == "add":
                            # print(op)
                            if re.match(r"^\/logs\/ChatOpenAI(?::\d+)?\/streamed_output\/\-$", op["path"]):
                                row_data = sse_json(op["value"].dict(exclude_unset=True)['content'])
                                yield json.dumps(row_data)

                            
            finally:
                yield json.dumps(sse_json('', finish_reason='stop'))
  

        return EventSourceResponse(stream_chat(db, user), media_type="text/event-stream")
    else:
        
        output = agent_executor.invoke(
            {"input": input_text,
            "chat_history": [convert_dict_to_message(message) for message in messages]
            }
            )                    
        return sse_json(output['output']) 
    


    
@router.post('/conversation/gen_title')
async def gen_title(request: Request):
    """修改对话的标题"""
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
    llm = ChatOpenAI(model="gpt-4o-mini", 
                     temperature=0, 
                     streaming=False
                     )
    title = llm.predict(prompt)
    return {'status':'Success', 'data':title}





    