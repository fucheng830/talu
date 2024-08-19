import json
from langchain.agents import create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from .load_tools import load_tools
from ..sse_format import sse_json

def load_agent(config, db):
    """初始化agent"""

    # 设置默认的llm
    llm = ChatOpenAI(**config.llm)

    tools = load_tools(config.tools, db)

    # 查看是否有知识库，如果有则加知识库tool
    if config.knowledge:
        @tool
        def knowledge_tool(query: str)-> str:
            """根据给定的查询字符串，从知识库中搜索相关文档，并返回合并后的文档内容。

    该函数使用了`search`方法来执行搜索操作。搜索依赖于配置中指定的知识库和数据库会话。
    搜索结果是一系列文档对象，这些对象包含了匹配查询的文档内容。
    最终，函数将所有找到的文档内容合并成一个字符串，并返回这个字符串。

    Args:
        query (str): 用户的查询字符串，用于在知识库中搜索相关文档。

    Returns:
        str: 搜索到的所有文档内容合并后的字符串。如果没有找到任何文档
            """
            from ..rag import search
            docs = search(query, config.knowledge[0]['uuid'], db)
            # 合并搜索的结果
            data = "\n".join([r.page_content for r in docs])
            return data
        
        tools.append(knowledge_tool)
        
    system_prompt = config.system_prompt

    if tools:
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

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    else:
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}")
        ]
        )
        agent_executor = prompt | llm

    return agent_executor 



async def stream_agent(agent_executor, messages, input_text, callback):
    try:
        async for event in agent_executor.astream_events(
            {"input_text": input_text,
            "msgs": messages}, version="v1"
        ):  
            final_output = ''
            if event:
                kind = event["event"]
                if kind == "on_chain_start":
                    if (
                        event["name"] == "Agent"
                    ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                        print(event)
                        print(
                            f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                        )
                elif kind == "on_chain_end":
                    if (
                        event["name"] == "AgentExecutor"
                    ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                        print(event)
                        print()
                        print("--")
                        print(
                            f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                        )
                        final_output+=event['data'].get('output')['output']
                    
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        # Empty content in the context of OpenAI means
                        # that the model is asking for a tool to be invoked.
                        # So we only print non-empty content
                        row_data = sse_json(content)
                        yield json.dumps(row_data)
                elif kind == "on_tool_start":
                    yield json.dumps(event)

                elif kind == "on_tool_end":
                    yield json.dumps(event)

           
    finally:
        yield json.dumps(sse_json('', finish_reason='stop'))
                # 在流结束后将回答存入数据库
        callback(final_output)



