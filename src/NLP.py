import os

from pylmkit.llms import ChatTongyi  # 阿里-通义
from pylmkit.perception.text import DocumentLoader
from pylmkit.llms import EmbeddingsHuggingFace
from langchain.vectorstores import FAISS
from pylmkit.app import DocRAG
from pylmkit.app import WebRAG

# # 阿里
# os.environ["DASHSCOPE_API_KEY"] = "DASHSCOPE_API_KEY"

# llm_model = ChatTongyi(model='qwen2-1.5b-instruct')
# llm_model = ChatTongyi(model='qwen-max')
llm_model = ChatTongyi(model='qwen-turbo', streaming=True)
# embed_model = EmbeddingsHuggingFace(model_name="../models/all-MiniLM-L6-v2")
embed_model = EmbeddingsHuggingFace(model_name="../models/average_word_embeddings_glove.840B.300d")
vdb_model = FAISS

with open('../res/raw_data - gbk.csv', 'r', encoding='gbk', errors='replace') as f:
    content = f.read()

with open('../res/rag_data.txt', 'w', encoding='utf-8', errors='replace') as f:
    f.write(content)

loader = DocumentLoader(path='../res/rag_data.txt')
docs = loader.split(chunk_size=200, chunk_overlap=50)

role_template = '你是北京师范大学的问答AI，你的名字是"京师大福"，与你对话的人是北师大的学生，你的工作是为北师大的师生解决实际问题，你要按照你已经知道的信息为北师大学生详细、准确地提供相关信息。每次对话你都要介绍一下你自己，并表示很乐意为你的对话者服务。'
prompt_list = [role_template]
rag = DocRAG(
    embed_model=embed_model,
    vdb_model=vdb_model,
    llm_model=llm_model,
    corpus=docs,
    show_language='中文',
    prompt_list=prompt_list,
    online_search_kwargs={}
)

while True:
    query = input("User query：")
    response, refer = rag.invoke(query
                                 , topk=10
                                 )
    print("\nAI：\n", response)
    # print("\nRefer：\n", refer)
