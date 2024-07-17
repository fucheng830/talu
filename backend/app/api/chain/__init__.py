


def base_llm(prompt, params, model="v1", temperature=0, streaming=False):
    from langchain_openai import ChatOpenAI
    """
    生成对话的总结标题。

    参数:
    model (str): 使用的模型名称。默认为 "v1"。
    temperature (float): 生成文本的温度，默认为 0。
    streaming (bool): 是否启用流式生成，默认为 False。

    返回:
    str: 生成的对话标题。
    """
    text = prompt.format(**params)
    
    llm = ChatOpenAI(model=model, temperature=temperature, streaming=streaming)
    return llm.predict(text)