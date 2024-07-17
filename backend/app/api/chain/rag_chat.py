# 基础基于对话类型的聊天机器人
# search, knowledge 

from langchain_openai import ChatOpenAI


def chain(knowledge, search):
    # 知识库
    if knowledge == "default":
        pass
    

    # 搜索引擎
    search = search

    # 聊天机器人
    chat_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | chat
        | StrOutputParser()
    )

    # 问答机器人
    qa_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | qa
        | StrOutputParser()
    )

    # 知识图谱
    knowledge_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | knowledge
        | StrOutputParser()
    )

    # 搜索引擎
    search_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | search
        | StrOutputParser()
    )

    return chat_chain, qa_chain, knowledge_chain, search_chain

def qa_chain():
    qa_chain = (
        {"context": context, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    return qa_chain
   

