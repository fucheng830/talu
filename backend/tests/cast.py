import requests
import json

def post_text_to_speech(input_text):
    url = "https://api.minimax.chat/v1/text_to_speech?GroupId=1768537645824098457"
    headers = {
        'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLljJfkuqzotqPmr5Tnibnnp5HmioDmnInpmZDlhazlj7giLCJVc2VyTmFtZSI6IuWMl-S6rOi2o-avlOeJueenkeaKgOaciemZkOWFrOWPuCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxNzY4NTM3NjQ1ODMyNDg3MDY1IiwiUGhvbmUiOiIxMzE2NDIwNzA4MCIsIkdyb3VwSUQiOiIxNzY4NTM3NjQ1ODI0MDk4NDU3IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMDMtMjMgMDQ6MjM6NDgiLCJpc3MiOiJtaW5pbWF4In0.Kn_D8u-1VtjYbgP3mqKwynoKXEVAD0uFOiF5P4HgSPY33vOrmV41pxY36B54LmCIPnDdRMB00QJss0D55XNEc3HGW1V3o74fvK38wnhZWG0aOGheqseaJBkg0hcl2kH5Y6GrmTb1TX9yif4JxIyDBFdDcX7uk5wYjw7CVS39mAE0scQsVgO3uxV8eHp2YwD3m0tYnfa509_q1F0fRrQFVmSMjFHvfOjmFHOHaXU55ze58ZfST61jcl5pEL2oLaqfWFrlZux038Xo0inPbR3Ddg3oDX_-l3TeKgclKBMD2-g011VEvnrt2mic6z40mLw_yr1M-2ZV8QC2hM3KMw7CBQ",
        'Content-Type': 'application/json',
    }
    data = {
        "voice_id": "male-qn-qingse",
        "text": input_text,
        "model": "speech-01",
        "speed": 1.0,
        "vol": 1.0,
        "pitch": 0,
        "timber_weights": [
            {"voice_id": "male-qn-qingse", "weight": 1},
            {"voice_id": "female-shaonv", "weight": 1},
            {"voice_id": "female-yujie", "weight": 1},
            {"voice_id": "audiobook_male_2", "weight": 1}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response

# 使用函数发送文本到语音转换请求
input_text = "你想转换的文本内容"
response = post_text_to_speech(input_text)

# 输出响应内容（根据实际情况，这里可能需要进一步的处理）
print(response.text)