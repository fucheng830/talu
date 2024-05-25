import re

def parse_query_from_url(url):
    # 解析URL中的查询参数字符串
    query_string = re.search(r'\?(.*)#', url).group(1)
    
    # 修正HTML实体编码
    query_string = query_string.replace('&amp;', '&')
    
    # 分割参数字符串为单独的参数
    query_params = query_string.split('&')
    
    # 创建一个字典存放每个参数的键值对
    params = {}
    for param in query_params:
        # 分割参数的键和值
        key, value = param.split('=', 1)
        params[key] = value
    
    return params

"""
基于给定的URL参数，以下是每个参数的可能含义：

1. `__biz`: 公众号的唯一标识（base64编码）。这是微信公众平台为每个公众号生成的唯一的标识符。

2. `mid`: 消息ID。这通常指的是微信公众号文章的消息ID。

3. `idx`: 文章在消息中的索引位置。`idx` 表示多图文消息的第几篇文章，1 通常是第一篇。

4. `sn`: 文章的唯一短链接后缀。`sn` 是一串哈希值，代表这篇文章的独特标识。

5. `chksm`: 校验参数，可能是用来验证文章链接的合法性。

6. `mpshare`: 表示这是一次分享行为，通常值为 '1' 表示已分享。

7. `scene`: 场景信息，该参数表明链接是在什么场景下被打开的。

8. `srcid`: 来源ID，可能用于跟踪文章的流量来源。

9. `sharer_shareinfo`: 分享者的分享信息，可能是分享者信息的加密字符串。

10. `sharer_shareinfo_first`: 第一次分享者的信息，可能是第一个分享这篇文章的用户信息的加密字符串。

这些参数通常用于统计分析，帮助公众号运营者了解他们的文章是如何被阅读和分享的。例如，运营者可以知道一个用户是通过哪个渠道（或哪个用户）来到他们的文章的。这些数据对优化内容推广策略非常重要。请注意，上面的解释是基于常识和公开可获取信息的推测，微信可能会有自己的内部标识和逻辑。
"""
# https://mp.weixin.qq.com/s/UrdRHBWxjCX6EDbQZ_3xWg
# 测试函数
# url = "http://mp.weixin.qq.com/s?__biz=Mzk0NDY0ODA5OA==&amp;mid=2247483831&amp;idx=1&amp;sn=f1ffbc7503db0a85836c324ee2de8f85&amp;chksm=c3203b7af457b26cf1119e28a5a3c9acd3c88d42016e44b20d40fc9a4026a4ec18532ca15a89&amp;mpshare=1&amp;scene=1&amp;srcid=0224YjipfgiikvG9s1ZN4ZMK&amp;sharer_shareinfo=b76ab4df1ea315095e89aea33f6a50a7&amp;sharer_shareinfo_first=b76ab4df1ea315095e89aea33f6a50a7#rd"
# parsed_params = parse_query_from_url(url)
# print(parsed_params)
# import requests
# data = requests.get(url, timeout=10)
# with open('test.html', 'w') as f:
#     f.write(data.text)

import re

# 定义正则表达式
pattern = r'https?:\/\/mp\.weixin\.qq\.com\/s(\?[\s\S]*)?'

# 测试字符串
text = ['https://mp.weixin.qq.com/s/DbkmFsB_4sE68fpRO_Fhng',
        'http://mp.weixin.qq.com/s?__biz=MzkxNDUyNDI4Ng==&amp;mid=2247485591&amp;idx=1&amp;sn=b9f0c69c85aa277dff2b0ed36e416c50&amp;chksm=c16c5986f61bd090b2fb5857b3a30c1e8c3886abd6c8c639fe5234044c9cc7bce60a71a0758b&amp;mpshare=1&amp;scene=1&amp;srcid=0224bdl3bwULcYQyAgtwdmBx&amp;sharer_shareinfo=d0fc23d1d5c2f342b180e8e74354299e&amp;sharer_shareinfo_first=addb161a8b185c75d58317da074472db#rd']




for r in text:
    print(re.match(pattern, r))
