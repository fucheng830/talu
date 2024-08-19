# 对话路由接口
from langchain_community.adapters.openai import convert_dict_to_message
from ...models import *
from .memory import embeddings_model, load_context_message


async def talk(params, db):
    """问答入口
    params:
        conversation_id 对话id
        stream 是否使用流的方式输出内容，默认为：True
        max_context_len 最大上下文长度，默认为：3
        context_compress_strage 上下文压缩策略，'keep_last' or 'rag' or 'summary'，默认为：'keep_last'
        user_id: 用户ID
        is_cot: 是否使用COT模式，默认为：False
    """
    if not params.conversation_id:
        conversation = Conversation(user_id=params.user_id, title=params.prompt)
        db.add(conversation)
        db.commit()
        params.conversation_id = conversation.id
    else:
        conversation = db.query(Conversation).filter_by(id=params.conversation_id).first()
        if not conversation:
            conversation = Conversation(user_id=params.user_id, title=params.prompt, id=params.conversation_id)
            db.add(conversation)
            db.commit()
            params.conversation_id = conversation.id

    # 插入问题到数据库
    prompt_embedding = embeddings_model.embed_query(params.prompt)
    messages = load_context_message(params.context_compress_strage, params.conversation_id, params.max_context_len, prompt_embedding, params.user_id, db)
    messages = [{"content": msg.content, "role": msg.role} for msg in messages]
    messages = [convert_dict_to_message(message) for message in messages]

    new_message = Message(
        conversation_id=params.conversation_id,
        user_id=params.user_id,
        content=params.prompt,
        embedding=prompt_embedding,
        role="user"
    )
    db.add(new_message)
    db.commit()

    def insert_answer(output):
        new_message = Message(
            conversation_id=params.conversation_id,
            user_id=params.user_id,
            content=output,
            embedding=embeddings_model.embed_query(output),
            role="assistant"
        )
        db.add(new_message)
        db.commit()

    
    return execute_agent(messages, params.prompt, insert_answer)

