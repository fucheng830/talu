import sys 
sys.path.append('/home/ubuntu/workspace/fucheng/ai_agents')

from app.database import SessionLocal, engine 
from app.models import *
from workspace.fucheng.ai_agents.src.application.web_browse import get_content_from_url
import requests
import io 
import base64
from PIL import Image as PILImage
import hashlib
from lxml import etree
import traceback
import re

from langchain.chat_models import ChatOpenAI


def prompt(template, **params):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
    PROMPT = template.format(**params)
    response = llm.predict(text=PROMPT)
    return response


def is_contain_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5\u3000-\u303f\uff01-\uff5e]')
    result = pattern.search(text)
    if result:
        return True
    else:
        return False


def transplot_prompt(text):
    template = """你是一个翻译官，请将以下内容翻译成中文：
    {content}
    """
    return prompt(template, content=text)



def auto_category(name, description):
    template = """你是一个自动分类器，你可以根据应用的描述自动生成类别标签。
    你可以选择的类别为：
    热门、画图、写作、营销、工具、研究与分析、编程、教育、生活娱乐、人物角色
    
    请根据以下描述，为其选择一个类别：
    应用名称: {name}
    应用描述: {description}
    请返回类别名称
    
    """
    return prompt(template, name=name, description=description)


def test():
    # 读取document表中的所有数据
    db = SessionLocal()
    agents = db.query(Agent).all()
    for row in agents:
        try:
            name = row.name
            description = row.description
            catgory = auto_category(name, description)
            row.category = catgory
            if not is_contain_chinese(description) and not is_contain_chinese(name):
                print(name, description)
                name = transplot_prompt(name)
                description = transplot_prompt(description)
                row.name = name
                row.description = description

            db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            # 删除错误的数据
            db.delete(row)

if __name__=='__main__':
    test()
