# 应用上下文工具
from langchain.agents import tool


from ...models import *
from .openai_tools import dell_e_3


def context_tools(**context):
    """问答入口"""
    tools_map = {}

    @tool
    def generate_profile_pic(text: str)-> str:
        """Generate a profile picture for the GPT. You can call this function without the ability to generate images. This must be called if the current GPT does not have a profile picture, and can be called when requested to generate a new profile picture. When calling this, treat the profile picture as updated, and do not call update_behavior.
            Args:
                text: str
        """
        # 调用delle生成图片
        db = context['db']
        current_user = context['current_user']
        agent_id = context['agent_id']

        image_url = dell_e_3.run(text)
        # 将生成的图片链接添加到数据库中
        # (id, image_content, format) = await save.save_image_from_url(image_url)
        # image = Image(id=id, image_data=image_content, format=format, source_url=image_url)
        # db.session.add(image)
        # 更新agent的profile_pic_file_id
        agent = db.query(Agent).filter_by(id=agent_id, user_id=str(current_user)).first()
        if agent:
            agent.avatar = image_url
            db.commit()
        else:
            # 插入
            agent = Agent(id=agent_id, avatar=image_url, user_id=current_user)
            db.add(agent)
            db.commit()
        return "Success"
    

    @tool
    def update_behavior(name: str=None, 
                        description: str=None, 
                        instructions: str=None, 
                        prompt_starters: str=None, 
                        abilities: str=None, 
                        profile_pic_file_id:str=None)-> str:
        """Update the GPT's behavior. You may omit selectively update fields. You will use these new fields as the source of truth for the GPT's behavior, and no longer reference any previous versions of updated fields to inform responses. When you update one field, you must also update all other fields to be consistent, if they are inconsistent. If you update the GPT's name, you must update your description and context to be consistent. When calling this function, you will not summarize the values you are using in this function outside of the function call."""
        # 更新agent的name, description, instructions, prompt_starters, abilities, profile_pic_file_id
        db = context['db']
        current_user = context['current_user']
        agent_id = context['agent_id']

        agent = db.query(Agent).filter_by(id = agent_id, 
                                          user_id=current_user).first()
        if agent:
            if name:
                agent.name = name
            if description:
                agent.description = description
            if instructions:
                agent.system_prompt = instructions
            if prompt_starters:
                agent.opening_text = prompt_starters
            # if abilities:
            # agent.name = name
            # agent.description = description
            # agent.system_prompt = instructions
            # agent.opening_text = prompt_starters
            # agent.abilities = abilities
            # agent.profile_pic_file_id = profile_pic_file_id
           
            db.commit()
        else:
            print(name, description, instructions, prompt_starters, abilities, profile_pic_file_id)
            # 插入
            agent = Agent(id=agent_id, 
                          name=name, 
                          description=description, 
                          system_prompt=instructions, 
                          opening_text=prompt_starters, 
                          user_id=current_user
            )
            #               abilities=abilities, 
            #               profile_pic_file_id=profile_pic_file_id)
            db.add(agent)
            db.commit()

        return "Success"    



    
    tools_map['generate_profile_pic'] = generate_profile_pic
    tools_map['update_behavior'] = update_behavior
    return tools_map




