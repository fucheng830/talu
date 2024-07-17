import requests
import os


def send(access_token, email, check_code):
    print("ckeck_code:", check_code)
    
    content = {
        "to": {
            "emails": [
                email,
            ],
        },
        "subject": "邮件验证码",
        "content": f"""
                <html>
                <body>
                    <h1 style="text-align: center; color: #333;">邮件验证码</h1>
                    <p>请使用以下验证码完成注册：</p>
                    <p class="code" style="text-align: center; font-size: 30px; font-weight: bold; color: #333;">{check_code}</p>
                    <p>验证码的有效期为10分钟，请尽快使用。</p>
                    <p style="text-align: center; margin-top: 20px;">如果您未申请过此验证码，请忽略此邮件。</p>
                </body>
                </html>
        """
    }
    req_data = {'content': content, 'access_token': access_token}
    WECHAT_SERVICE_URL = os.environ.get("WECHAT_SERVICE_URL")
    res = requests.post(f'{WECHAT_SERVICE_URL}/send_mail', json=req_data)
    if res.status_code==200:
        print(res.json())
    return True


