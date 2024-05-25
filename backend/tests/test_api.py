import requests
import uuid
import random
import string

# The base URL where your FastAPI application is running
BASE_URL = "http://127.0.0.1:8003"
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    

def random_string(length=10):
    """Generate a random string of letters and digits"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def random_email():
    """Generate a random email"""
    domains = ["example.com", "test.com", "sample.org", "demo.net"]
    return random_string(7) + "@" + random.choice(domains)

def test_create_user():
    url = f"{BASE_URL}/users/"
    user_data = {
        "user_id": str(uuid.uuid4()),  # Generate a new UUID for each test user
        "union_id": random_string(12),
        "openid": random_string(12),
        "name": "Test User " + random_string(5),
        "avatar": "http://example.com/avatar.jpg",
        "subscribe_scene": "Test Scene",
        "password": "password",
        "phone_num": ''.join(random.choice(string.digits) for _ in range(10)),
        "session_key": "session_key",
        "vip_end_time": "2023-01-01T00:00:00",
        "status": 1,
        "register_time": "2023-01-01T00:00:00",
        "user_info": {},
        "email": random_email(),
        "referee": str(uuid.uuid4()),
        "ip": "127.0.0.1"
    }
    response = requests.post(url, json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_data["user_id"]
    return data["user_id"]

def test_read_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id

def test_login():
    url = f"{BASE_URL}/login"
    login_data = {
        "email": "admin@example.com",
        "password": "secure_admin_password"
    }
    response = requests.post(url, json=login_data)
    assert response.status_code == 200
    data = response.json()
    print(data)


def test_save_content():
    input_text = 'https://mp.weixin.qq.com/s/Imk7UvjtumMNgYp68hnHLg'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f'{BASE_URL}/save_content_from_link', json={"url": input_text}, headers=headers)
    if response.status_code == 200:
        print('保存成功')
    else:
        print(response.text)

def test_get_content():
    input_text = 'https://www.toutiao.com/article/7320165505309393443/?log_from=fd22f7fab5849_1704383867197'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f'{BASE_URL}/get_content/', json={"url": input_text}, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def test_search():
    input_text = 'Agents'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f'{BASE_URL}/search_content/', json={"text": input_text}, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def test_chat():
    while True:
        input_text = input('请输入：')

        # input_text = '请帮我保存一个网页：https://mp.weixin.qq.com/s/Imk7UvjtumMNgYp68hnHLg'
        # input_text = '请帮我画一个美女图'
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(f'{BASE_URL}/v1/chat/completions', json={"messages": [
            {'content':input_text}
            
            ]}, headers=headers)
        if response.status_code == 200:
            for r in response.iter_lines():
                print(r.decode('utf-8'))
        else:
            print(response.text)

def test_app_chat():
    while True:
        input_text = input('请输入：')

        # input_text = '请帮我保存一个网页：https://mp.weixin.qq.com/s/Imk7UvjtumMNgYp68hnHLg'
        # input_text = '请帮我画一个美女图'
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(f'{BASE_URL}/43c7076a-861f-4454-8047-cd55afc0fef2/v1/chat/completions', json={"messages": [
            {'content':input_text}
            
            ]}, headers=headers)
        if response.status_code == 200:
            for r in response.iter_lines():
                print(r.decode('utf-8'))
        else:
            print(response.text)
        

def test_get_documents():

    url = f'{BASE_URL}/documents'  # 修改为实际运行的 FastAPI 应用的 URL
    payload = {
        "skip": 0,
        "limit": 10
    }
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print("Response:", response.json())





def test_add_agent():
    url = f'{BASE_URL}/add_agent'

    # 假设已经有一个名为agent的字典对象，用于传递给接口
    agent = {
        "name": "测试Agent",
        "description": "Agent Description",
        "starter": [],
        "knowledge": [],
        "tools": [],
        "voice": "Agent Voice",
        "avatar": "Agent Avatar",
        "suggestion": [],
        "permission": "Agent Permission",
    }
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(url, json=agent, headers=headers)

    # 检查返回的状态码是否为200（表示成功）
    if response.status_code == 200:
        print('Agent added successfully')
    else:
        print('Failed to add agent')
        print(response.json())


def test_add_gpt_agents():
    import pandas as pd
    # i = 0
    # datas = []
    # while True:
    #     try:
    #         if i>100:
    #             break
    #         res = requests.get(f'https://gpts.ddaiai.com/open/gptsapi/list/{i}') 
    #         if res.status_code==200:
    #             data = res.json()
    #             if data['data']['list']:
    #                 datas.extend(data['data']['list'])
    #                 i += 1
    #                 print(i)
    #                 print(len(datas))
    #             else:
    #                 break
    #     except Exception as e:
    #         print(e)
    #         break

    # pd.DataFrame(datas).to_csv('gpt_agents.csv', index=False)

    df = pd.read_csv('gpt_agents.csv')
    df = df.drop_duplicates(subset='gid')
    print(len(df))
    for i, row in df.iterrows():
        try:
            config = row.to_dict()
            image_url = config['logo']
            image_data = upload_image(image_url)

            agent_config = {
                'gid':config['gid'],
                'name':config['name'],
                'description':config['info'],
                'starter':[],
                'knowledge':[],
                'tools':[],
                'voice':'',
                'avatar':'https://site.123qiming.com'+image_data['data']['image_url'],
                'suggestion':[],
                'permission':'public',
                'category':'writer',
                'system_prompt':'',
                'llm':{}
            }

            url = f'{BASE_URL}/add_agent'
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.post(url, json=agent_config, headers=headers)

            # 检查返回的状态码是否为200（表示成功）
            if response.status_code == 200:
                print('Agent added successfully')
            else:
                print('Failed to add agent')
                print(response.text)

        except Exception as e:
            print(e)


def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open("temp.jpg", 'wb') as f:
            f.write(response.content)
        return True
    return False

def upload_image(image_url):
    import os
    download_image(image_url)

    url = f'{BASE_URL}/upload_image'
    file_path = "temp.jpg"  # 你要上传的图片的路径

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)
    
    return response.json()
    

def test_get_agents():
    url = f'{BASE_URL}/agents'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json={}, headers=headers)
    print(response.json())


def test_web_browse():
    url = f'{BASE_URL}/web_browse'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, params={'url':'https://mp.weixin.qq.com/s/IdFpWoLve_EAWHh1Bry87w'}, headers=headers)
    print(response.json())    


def test_upload_file():
    url = f'{BASE_URL}/upload_file'
    file_path = 'temp.jpg'
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Define the files parameter for the request
        files = {'file': (file_path, f)}
        
        # Define the headers including the authorization token if provided
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        
        # Send the request
        response = requests.post(url, files=files, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print('File uploaded successfully:', response.json())
        else:
            print('Failed to upload the file:', response.status_code, response.text)    


def test_add_manual_container():
    api_url = f'{BASE_URL}/add_manual_container'
    # 构造请求体
    data = {
        "name": "测试容器",
        "knowledge_id": '9e48f507-7e12-49d6-aa25-40e83099e7e7'  # 假设knowledge_id是一个UUID字符串
    }

    # 设置认证令牌，假设使用Bearer Token认证
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(api_url, json=data, headers=headers)

    # 将响应结果返回
    print(response.json())


def test_add_manual_document():
    """
    测试添加手动文档的接口。

    参数:
    - api_url: 接口的URL。
    - auth_token: 用于认证的令牌。
    - document_content: 包含文档内容的字典。
    """
    api_url = f'{BASE_URL}/add_manual_document'
    # 设置请求头，包括认证令牌和内容类型
    document_content = {
        "content": "测试文档",
        "user_id": "598a7fd4-6bff-4f07-918a-f07e452ab050",
        "group_id": "598a7fd4-6bff-4f07-918a-f07e452ab050",
        "knowledge_id": "9e48f507-7e12-49d6-aa25-40e83099e7e7",
        "node_id": "9e48f507-7e12-49d6-aa25-40e83099e7e7",
    }   
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(api_url, json=document_content, headers=headers)

    # 返回响应状态码和响应体
    print(response.json())


def test_search_node():
    api_url = f'{BASE_URL}/search_node'
    # 构造请求体
    data = {
        "query": "奖惩",
        "knowledge_id": '9e48f507-7e12-49d6-aa25-40e83099e7e7'  # 假设knowledge_id是一个UUID字符串
    }

    # 设置认证令牌，假设使用Bearer Token认证
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(api_url, json=data, headers=headers)

    # 将响应结果返回
    print(response.json())

def test_agent_edit():
    api_url = f'{BASE_URL}/agent_edit'
    # 构造请求体
    data =  {
        "id": str(uuid.uuid4()),
        "name": "测试agent",
        "description": "test_description",
        "starter": ["starter1", "starter2"],
        "system_prompt": "test_system_prompt",
        "knowledge": ["knowledge1", "knowledge2"],
        "tools": ["tool1", "tool2"],
        "voice": "test_voice",
        "avatar": "test_avatar",
        "suggestion": ["suggestion1", "suggestion2"],
        "permission": "test_permission",
        "category": "test_category",
        "gid": "test_gid"
    }
    # 设置认证令牌，假设使用Bearer Token认证
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(api_url, json=data, headers=headers)

    # 将响应结果返回
    print(response.json())

def test_pay():
    api_url = f'{BASE_URL}/pay'
    # 构造请求体
    data =  {
        "plan_id": 1,
    }
    # 设置认证令牌，假设使用Bearer Token认证
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 发送POST请求
    response = requests.post(api_url, json=data, headers=headers)

    # 将响应结果返回
    print(response.json())


if __name__ == "__main__":
    # print("Testing user creation...")
    # user_id = test_create_user()
    # print("Testing user retrieval...")
    # test_read_user(user_id)
    # print("Tests completed successfully!")
    # test_login()
    # test_save_content()
    # test_chat()
    # test_app_chat()
    # test_get_documents()
    # print(upload_image("http://192.168.2.150:5173/src/assets/logo.png"))
    import sys 
    if len(sys.argv) > 1:
        eval(sys.argv[1])()

    
