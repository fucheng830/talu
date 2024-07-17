from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter

def split_markdown_text(text, chunk_size=1000, chunk_overlap=30):
    """
    递归拆分 Markdown 格式文本。
    
    参数:
    text (str): Markdown 格式的文本
    chunk_size (int): 每个块的最大长度
    chunk_overlap (int): 相邻块之间的重叠长度
    
    返回:
    list[Document]: 拆分后的 Document 对象列表
    """
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
        ("- ", "Unordered List Item"),
        ("* ", "Unordered List Item"),
        ("1. ", "Ordered List Item"),
        ("```", "Code Block"),
    ]
    
    # 创建 Markdown 文本分割器
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    
    # 先按 Markdown 头部拆分
    md_header_splits = markdown_splitter.split_text(text)
    
    # 再按字符级别递归拆分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # 拆分每个按头部拆分的段落
    documents = []
    for md_split in md_header_splits:
        split_docs = text_splitter.create_documents([md_split.page_content])
        documents.extend(split_docs)
    
    return documents

if __name__=='__main__':
    # 示例使用
    markdown_document = """# Intro 

    ## History 

    Markdown[9] is a lightweight markup language for creating formatted text using a plain-text editor. John Gruber created Markdown in 2004 as a markup language that is appealing to human readers in its source code form.[9] 

    Markdown is widely used in blogging, instant messaging, online forums, collaborative software, documentation pages, and readme files. 

    ## Rise and divergence 

    As Markdown popularity grew rapidly, many Markdown implementations appeared, driven mostly by the need for 

    additional features such as tables, footnotes, definition lists,[note 1] and Markdown inside HTML blocks. 

    #### Standardization 

    From 2012, a group of people, including Jeff Atwood and John MacFarlane, launched what Atwood characterised as a standardisation effort. 

    ## Implementations 

    Implementations of Markdown are available for over a dozen programming languages.
    """

    # 调用函数进行拆分
    documents = split_markdown_text(markdown_document)
    for doc in documents:
        print(doc.page_content)


