from ..loadlib import import_from_string
from ...models import ToolConfig

from langchain.agents import Tool

def load_tools(tools_config, db):
    tools = []
    # 查询在tools_config中的id
    if tools_config:
        tools_list = db.query(ToolConfig).filter(ToolConfig.id.in_(tools_config)).all()
        for tool_config in tools_list:
            tool_config = tool_config.__dict__
            tool_module = import_from_string(tool_config['code'], 'default_tool')
            func = getattr(tool_module, tool_config['func'])
            tool_obj = Tool(
                tool_config['name'],
                func,
                tool_config['description'],
            )
            tools.append(tool_obj)
    return tools
