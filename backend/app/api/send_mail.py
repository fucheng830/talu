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


def send_ad_email(to, access_token, subject, ad_content):
    content = {
        "to": {
            "emails": [
                to,
            ],
        },
        "subject": subject,
        "content": ad_content
    }
    req_data = {'content': content, 'access_token': access_token}    
    res = requests.post('http://101.35.246.108:6040/send_mail', json=req_data)
    if res.status_code==200:
        print(res.json())
     
        
if __name__=='__main__':
    access_token = 'hIgy-1NVCP1uCS25dGOqxWiQg_DIK3aFTWUfJqqQrznasLfi4Xkfyw-jVfaUlgXoEl-hE25PklDekVqFsO8dqvGtcQVK2oHsV8cpEXJ7oZ450YAnE6E059jprX5JBu2GL_g3I8qink-qSajqXQc96OvGAGSc-wX1rGUx1in5_5Zrd9gNHg1miq_77kzxsLVJNaPPI2cyI8JGZxKDfsf17g'
    email = 'fucheng@123qiming.com'
    content = '''
<!DOCTYPE html>
<html>
<head>
<title>使用新产品邮件</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<div style="background-color: #f2f2f2; padding: 20px;">
<h1>尊敬的用户，</h1>
<p>我们很高兴地向您介绍，我们上线了新版本！</p>
<p>我们的新版本增加了模型选择功能，并且支持gpt-4模型，支持对话中添加知识库和更多的设置功能</p>
<p>我们相信，您会喜欢这款产品，并且在使用它的过程中获得更多的价值。</p>
    <p>如果您有任何问题或建议，请随时联系我们的客服团队。<a href="https://work.weixin.qq.com/kfid/kfcf34773bc3f87c4f1">客服</a></p>
    <a class="button" href="http://chat.123qiming.com">立即使用</a>
<p>谢谢！</p>
<p>最好的问候，</p>
<p>Quchat团队</p>
<p>chat.123qiming.com</p>
<p>关注公众号</p>
<img src="http://chat.123qiming.com/assets/gzh-3d665c0a.png">
</div>
</body>
</html>
'''
    # from web_server import app, db, User
    # with app.app_context():
        # result = db.session.query(User).filter_by(vip_end_time=None).all()
        # for r in result:
            # print(r.email)
    send_ad_email(access_token, email, content)
