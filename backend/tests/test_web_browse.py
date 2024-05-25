from src.application.web_browse.browse import get_content_from_url

async def test():
    url = 'https://www.toutiao.com/article/7320165505309393443/?log_from=fd22f7fab5849_1704383867197'
    # url = 'https://mp.weixin.qq.com/s/y_fK3RTCCHcedUcY26y5fQ'
    # url = 'http://www.aitop66.com/'
    content = await get_content_from_url(url)
    print(content)



if __name__=='__main__':
    import asyncio
    asyncio.run(test())