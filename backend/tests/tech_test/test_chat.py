from openai import OpenAI

data = {"messages": 
        [{"role": "system", 
          "content": """
            
    # 背景
        你是一个编程助手，你的工作是为程序员提供代码编写服务。
   
    
    # 执行过程
        1. 根据用户提出的问题，自动根据需求搜索代码上下文
        2. 根据需求编写代码
        3. 保存代码到指定目录
          """},
        {"role": "user", "content": "你好"}], 
        "model": "gpt-4-1106-preview", 
        "n": 1, 
        "stream": False, 
        "temperature": 0.0, 
        "tools": [{"type": "function", "function": {"name": "retriever_tool", "description": "retriever_tool(query: str) -> str - \u901a\u8fc7\u67e5\u8be2\u68c0\u7d22\u76f8\u5173\u6587\u6863", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}]
        }

client = OpenAI(
    api_key="sk-2YIT9ALUSqepiChpF947A14dFb5d4bD89c54B7Fc1e755fBd",
    base_url="https://api.zyai.online/v1"
)


response = client.chat.completions.create(
**data
)

print(response.choices[0].message.content)


