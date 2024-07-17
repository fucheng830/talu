from fastapi import HTTPException
import requests
from lxml import etree
import html2text

def replace_image(img):
    url = img.get('data-src')
    markdown_img = f"![image](http://images.aitop66.com/{url})"
    new_element = etree.Element("p")
    new_element.text = markdown_img
    try:
        img.getparent().replace(img, new_element)
    except Exception as e:
        print(e)
    print(f"Replaced image {url} with {markdown_img}")

def process_images(content):
    images = content.xpath('.//img')
    for img in images:
        img_url = img.get('data-src')
        if img_url:
            # Schedule replace_image for execution
            replace_image(img)
        

def read_url(url: str):
    """
    Read the content from the url and return the content.
    """
    if 'mp.weixin.qq.com' in url:
        return read_gzh(url)
    else:
        return read_other(url)


def read_gzh(url: str):
    """
    Read the content from the url and return the content.
    """
    URL_BASE = "http://192.168.1.11:8001"
    end_point = f"{URL_BASE}/fetch_page"
    response = requests.post(end_point, json={"url": url})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        data = response.json()
        content_html = data["data"]
        html = etree.HTML(content_html)
        title = html.xpath('//meta[@property="og:title"]/@content')[0]
        head_img = html.xpath('//meta[@property="og:image"]/@content')[0]
        description = html.xpath('//meta[@property="og:description"]/@content')[0]
        content = html.xpath('//div[@id="js_content"]')[0]
        process_images(content)
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        text_maker.images_to_alt = True  # 将图片转换为其alt文本
        markdown = text_maker.handle(etree.tostring(content, pretty_print=True).decode())
        return {'title': title, 'head_img': head_img, 'description': description, 'content': markdown}


def read_other(url: str):
    """
    Read the content from the url and return the content.
    """
    new_url = f"https://r.jina.ai/{url}"
    response = requests.get(url, headers={"User-accept": "text/json"})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        data = response.json()
        return data

    
