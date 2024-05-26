from langchain.utilities.dalle_image_generator import DallEAPIWrapper

dell_e_3 = DallEAPIWrapper()
dell_e_3.model_name = 'dall-e-3'
tool_main = dell_e_3.run

