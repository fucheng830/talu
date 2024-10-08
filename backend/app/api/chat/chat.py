# 对话型应用，支持模型动态选择，支持提示词动态选择，支持上下文参数选择，支持模型参数选择，支持tools选择，支持api开放
# chain 架构，非Agent架构

def load_llm(llm_config):
    # 假设使用LangChain加载LLM
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=llm_config['model'], temperature=llm_config['temperature'])


def load_tools(tools_config):
    # 加载工具
    tools = {}
    for tool in tools_config:
        tools[tool['name']] = {
            'description': tool['description'],
            'parameters': tool['parameters']
        }
    return tools

def load_chat_prompt(prompt):
    # 加载聊天提示
    from langchain_core.prompts import PromptTemplate
    return PromptTemplate.from_template(prompt)

def load_file_path(file_path):
    # 处理文件路径
    return file_path  # 这里可以根据需要进行处理




    # 'file_path': 'file_path',



# def create_chat_chain():
#     llm = load_llm(config['llm'])
#     memory = load_memory(config['context'])
#     tools = load_tools(config['tools'])
#     prompt = load_chat_prompt(config['prompt'])
#     file_path = load_file_path(config['file_path'])

#     return llm, memory, tools, prompt, file_path


