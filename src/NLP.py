import os

# 阿里


from pylmkit.llms import ChatTongyi  # 阿里-通义

llm_model = ChatTongyi()

from pylmkit.perception.text import DocumentLoader
loader = DocumentLoader(path='../res/raw_data - utf-8.csv')
docs = loader.split(chunk_size=200, chunk_overlap=50)

# 本地调用
from pylmkit.llms import EmbeddingsHuggingFace  # 使用 HuggingFace 中开源模型

# 本案例使用本地模型，为了方便使用一个小模型（下载模型一般会下载超时，需合理上网）
embed_model = EmbeddingsHuggingFace(model_name="all-MiniLM-L6-v2")

from langchain.vectorstores import FAISS
vdb_model = FAISS

from pylmkit.app import DocRAG
from pylmkit.app import WebRAG


# 角色模板可以根据自己情况进行设计，这是一个简单例子
role_template = "{ra}\n user question: {query}"
rag = DocRAG(
    embed_model=embed_model,
    vdb_model=vdb_model,
    llm_model=llm_model,
    corpus=docs,
    role_template=role_template,
    return_language="中文",
    online_search_kwargs={},
    # online_search_kwargs={'topk': 2, 'timeout': 20},  # 搜索引擎配置，不开启则可以设置为 online_search_kwargs={}
)

while True:
    query = input("User query：")
    response, refer = rag.invoke(query, topk=10)  # 使用检索最相似的topk=10个
    print("\nAI：\n", response)
    print("\nRefer：\n", refer)


