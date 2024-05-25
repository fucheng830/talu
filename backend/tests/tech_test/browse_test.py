from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
loader = AsyncChromiumLoader(["https://www.toutiao.com/article/7320165505309393443/?log_from=fd22f7fab5849_1704383867197"])
html = loader.load()
print(html)