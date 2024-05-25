
def arxiv():
    from langchain_community.utilities import ArxivAPIWrapper
    arxiv = ArxivAPIWrapper()
    docs = arxiv.run("1605.08386")
    print(docs)


if __name__=='__main__':
    import sys
    eval(sys.argv[1])()