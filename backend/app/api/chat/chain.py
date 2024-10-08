import json
import time
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from sse_starlette.sse import EventSourceResponse

from ..sse_format import sse_json


def load_executor(**config):
    """通过配置加载执行器
    config = {
    'llm': {
        'model': 'gpt-4o-mini', # 模型
        'temperature': 0.5, # 温度
    },
    'system_prompt': 'You are a prompt engineer, please analyze the prompt and give me the prompt list',
    'tools': [
        {
            'name': 'rag',
            'description': '搜索知识库的数据',
            'parameters': {
                'type': 'object',
                'properties': {
                    'prompt': {'type': 'string'},
                },
                'required': ['prompt'],
            },
        },
        {
            'search': 'search',
            'description': '搜索公开数据',
            'parameters': {
                'type': 'object',
                'properties': {
                    'prompt': {'type': 'string'},
                },
                'required': ['prompt'],
            },
        }
    ],
    'prompt': '{input}',
}
    """

    system_prompt = config.get("system_prompt", "")

    llm_config = config.get("llm", {'model': 'gpt-4o-mini', 'temperature': 0.5})

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("msgs"),
        ]
    )
    llm = ChatOpenAI(**llm_config)
    agent_executor = prompt_template | llm
    return agent_executor


async def stream_chat(agent_executor, messages, callback):
    start_time = time.time()
    try:
        final_output = ""
        async for chunk in agent_executor.astream(
            {"msgs": messages}
        ):
            if chunk:
                row_data = sse_json(chunk.content)
                final_output += chunk.content
                yield json.dumps(row_data)

    except Exception as e:
        yield json.dumps(sse_json(str(e), finish_reason="error"))
    finally:
        yield json.dumps(sse_json("", finish_reason="stop"))
        execution_time = time.time() - start_time
        print(f"执行链时间: {execution_time:.4f}秒")
        callback(final_output)


def execute_chain(agent_executor, messages, callback, stream=True):
    if stream:
        return EventSourceResponse(
            stream_chat(agent_executor, messages, callback),
            media_type="text/event-stream",
        )
    else:
        output = agent_executor.invoke({"msgs": messages})
        return sse_json(output["output"])


