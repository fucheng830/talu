"""
加载文档模块，用于加载文档
"""
from langchain_community.document_loaders import Docx2txtLoader


def load_word(path):
    loader = Docx2txtLoader(path)
    return loader.load()


def load_csv(path):
    from langchain_community.document_loaders.csv_loader import CSVLoader
    loader = CSVLoader(path)
    return loader.load()


def load_pdf(path):
    from langchain_community.document_loaders import MathpixPDFLoader
    loader = MathpixPDFLoader(path)
    return loader.load()


def load_excel():
    pass


def load_ppt():
    pass


def load_txt():
    pass


def load_image(src):
    with open(src, 'rb') as f:
        return f.read()


def load_video():
    pass


def load_audio():
    pass


def load_document():
    pass

def load_markdown(path):
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    loader = UnstructuredMarkdownLoader(path)
    return loader.load()


if __name__=='__main__':
    print(load_image('https://site.123qiming.com/image/fcc9891a6dbb832b2fe9fc0dd4fdddbb.jpg'))