from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

# 引入tool
from langchain.tools import tool

from langchain.tools.retriever import create_retriever_tool
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy

from db import Session, Node

embeddings_model = OpenAIEmbeddings()

store = PGVector(
    connection_string='postgresql://postgres:Fucheng830@192.168.2.152:5433/postgres', 
    embedding_function=embeddings_model, 
    collection_name='Navie UI',
    distance_strategy=DistanceStrategy.COSINE
)

retriever = store.as_retriever(search_kwargs={'k': 5})


# 自动写代码agent

# 定义tools
def chat(model='gpt-4-0125-preview', temperature=0, streaming=False):
    """问答入口"""

    llm = ChatOpenAI(model=model, 
                     temperature=temperature, 
                     streaming=streaming,
                     )

    @tool
    def retriever_tool(query: str) -> str:
        """通过查询检索相关文档
        """
        contents = []
        doc_ids = []
        for r in retriever.get_relevant_documents(query):
            doc_ids.append(str(r.metadata['doc_id']))
        
        with Session() as session:
            all_nodes = session.query(Node).filter(Node.node_id.in_(doc_ids)).all()
            for node in all_nodes:
                if node.node_type=='file':
                    file_content = node.data['file_content']
                    contents.append(file_content)
                    
        content = '\n\n'.join(contents)
        return content
      
    

    tools = [retriever_tool]

    system_prompt = """
    # 背景
        你是一个编程助手，你的工作是为程序员提供代码编写服务。
   
    
    # 执行过程
        1. 根据用户提出的问题，自动根据需求搜索代码上下文
        2. 根据需求编写代码
        3. 保存代码到指定目录
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
    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


    return agent_executor


if __name__=='__main__':
    while True:
        prompt = input("请输入你的问题：")
        agent = chat()
        agent.invoke({"input": prompt})



