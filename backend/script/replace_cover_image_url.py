import sys 
sys.path.append('/home/ubuntu/workspace/fucheng/ai_agents')

from src.database import SessionLocal, engine 
from src.models import *
from workspace.fucheng.ai_agents.src.application.web_browse import get_content_from_url
import requests
import io 
import base64
from PIL import Image as PILImage
import hashlib
from lxml import etree
import traceback

def image_to_base64(image_content, ext):
    # 将图片内容转换为Base64编码
    return 'data:image/{};base64,{}'.format(ext, base64.b64encode(image_content).decode())


def download_image(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None


def replace_image(url):

    image_content = download_image(url)
    if image_content:
        # Prepare for uploading the image and saving it to the database
        image_content_file = io.BytesIO(image_content)
        md5_hash = hashlib.md5()
        md5_hash.update(image_content)
        id = md5_hash.hexdigest()
        try:
            image_format = PILImage.open(image_content_file).format
        except IOError:
            return None

    return (id, image_content, image_format.lower(), url)



# 读取document表中的所有数据
db = SessionLocal()
documents = db.query(Document).all()
print(len(documents))

for row in documents:
    if 'id' in row.cover_image_url:
        try:
            print(row.source['url'])
            origin_url = row.source['url']
            res = requests.get(origin_url, timeout=20)
            if res.status_code != 200:
                continue
            html = etree.HTML(res.content)
            head_img = html.xpath('//meta[@property="og:image"]/@content')[0] if html.xpath('//meta[@property="og:image"]/@content') else None
            description = html.xpath('//meta[@property="og:description"]/@content')[0] if html.xpath('//meta[@property="og:description"]/@content') else None
            author = html.xpath('//meta[@property="og:article:author"]/@content')[0] if html.xpath('//meta[@property="og:article:author"]/@content') else None
            
            # 将cover_image_url中的http://localhost:8000替换为http://
            id, image_content, image_format, url = replace_image(head_img)

            def save_image_to_database(image_data):
                id, content, format, url = image_data
                # Save the image to the database
                result = db.query(Image).filter_by(id=id).first()
                if not result:
                    new_image = Image(
                        id=id,
                        image_data=content,
                        format=format,
                        source_url=url,
                    )
                    db.add(new_image)
                    db.commit()

                return f'https://site.123qiming.com/image/{id}.{format}'
            
            print(row.document_id)
            new_url = save_image_to_database((id, image_content, image_format, url))
            row.cover_image_url = new_url
            row.author = author
            db.commit()
            print(f"Replaced image {url} with {new_url}")
        except Exception as e:
            traceback.print_exc()

            