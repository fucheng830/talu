import markdown
from lxml import etree

def extract_images_and_context_with_xpath(markdown_text):
    # 将Markdown文本转换为HTML
    html = markdown.markdown(markdown_text)

    # 使用lxml构建解析树
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)

    # 使用XPath定位图片和相应文本的元素
    image_context = []
    image_tags = tree.xpath('//img[@src]')
    
    for idx, img_tag in enumerate(image_tags):
        image_url = img_tag.attrib['src']
        
        # 获取图片标签前面的文本，直到上一个图片标签
        context = ""
        if idx > 0:
            prev_img_tag = image_tags[idx - 1]
            preceding_text = tree.xpath('string(./preceding::text()[preceding::img[@src="%s"]])' % prev_img_tag.attrib['src'])
            context = preceding_text.strip()

        image_context.append({'image_url': image_url, 'context_text': context})
    
    return image_context

# Markdown文本示例
markdown_text = '''
更好地理解人类的隐含需求和期望。因为整个系统的效率和有效性很大程度上依赖于 LLMs 的准确性...

![image](https://site.123qiming.com/image/56b3589cd7594b21dbc7583bdc2e4504.png)

此外，Lilian Weng（Open AI的成员）对Agent有一个定义：Agent = LLMs（大语言模型）+ Memory（记忆）+ Planning skills（规划能力）+ Tool use（工具使用）...

![image](https://site.123qiming.com/image/aa6320ff53c712b0f84712204d847e27.png)

其中 Memory 就是另一方面的问题，一方面尽管现在有高达 100K 的上下文大模型，但是其费用消耗依然不是能够批量推广的。因此目前就需要依赖 Prompt 和本地或向量存储（AutoGPT 就放弃了向量存储）的组合来解决，而如何组合和搭配能够提供最多可用的上下文和最大程度的减少消耗也依然是一个非常大的课题。
'''

# 提取图片和文本上下文
image_context_list = extract_images_and_context_with_xpath(markdown_text)

# 打印每张图片及其上下文文本
for idx, image_context in enumerate(image_context_list, 1):
    print(f"Image {idx}:")
    print(f"Image URL: {image_context['image_url']}")
    print(f"Context Text:\n{image_context['context_text']}\n")
