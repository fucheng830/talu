
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import requests

text_splitter = SemanticChunker(OpenAIEmbeddings())

