import requests 

while True:
    try:
        input_text = input('请输入：')
        if input_text == 'exit':
            break
        # 增加请求头 token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTk4YTdmZDQtNmJmZi00ZjA3LTkxOGEtZjA3ZTQ1MmFiMDUwIiwicGFzc3dvcmQiOiJzZWN1cmVfYWRtaW5fcGFzc3dvcmQiLCJleHAiOjE3MTk3NjY3MjZ9.PN-vP6XUAX6FdwBqMQVEqUXtbVT_dHoU47yxWcFJjpQ'
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post('https://site.123qiming.com/save_content_from_link', json={"url": input_text}, headers=headers)
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)
    except Exception as e:
        print(e)
        