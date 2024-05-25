from langchain.chat_models import ChatOpenAI
from langchain.agents import tool

from langchain.callbacks.base import BaseCallbackHandler
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.agents import Tool
from langchain.agents import AgentExecutor, tool
import requests


llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, streaming=True)

dell_e_3 = DallEAPIWrapper()
dell_e_3.model_name = 'dall-e-3'

image_generate = Tool(
    "Dall-E-Image-Generator",
    dell_e_3.run,
    "A wrapper around OpenAI DALL-E API. Useful for when you need to generate images from a text description. Input should be an image description.",
)


@tool
def save_content(url: str)->str:
    """用户可以输入一个url, 然后自动解析url的文章，将文章保存到数据库中，并且生成向量索引嗯"""
    try:
        print(f"保存了一个网址: {url} ")
        headers = {"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ"}
        res = requests.post('http://site.123qiming.com/save_content_from_link', json={url:url}, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return '抱歉保存出现问题'


@tool
def search_content(text: str)->str:
    """根据用户的数据，搜索数据库中最相关的文章"""
    print(f"搜索了一个关键词: {text}")
    return f"已经正确搜索{text}"




tools = [save_content, search_content, image_generate]


from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

sysytem_en='''You are a powerful assistant who can use function calls to autonomously invoke tools based on user input. 
For example, you can save a website for me. When a user inputs a URL, you can automatically call the save-content tool to store that URL.
'''


system_prompt = """
你是一位强大的助手，能够根据用户输入自动调用工具来执行各种任务。
例如:
你可以为我保存一个网站。当用户输入一个URL时，你可以自动调用保存内容工具来存储该URL。
你可以调用工具读取网页链接，并且将其保存到数据库中。
你还可以搜索文章，当用户输入一个关键词，你可以自动调用搜索工具，搜索数据库中最相关的文章。
你还可以生成图片，当用户输入一个图片描述，你可以自动调用生成图片工具，生成一张图片。
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


from langchain.tools.render import format_tool_to_openai_function

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent.save(file_path="path/agent.yaml")


