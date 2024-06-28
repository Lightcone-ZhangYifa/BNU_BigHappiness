import os
import time
import pylmkit
from dotenv import load_dotenv
from pylmkit.app import RolePlay
from pylmkit.llms import ChatTongyi  # 阿里-通义
from pylmkit.web.webui import RAGWebUI, BaseWebUI
from pylmkit.memory import MemoryHistoryLength
from pylmkit.perception.text import DocumentLoader
from pylmkit.llms import EmbeddingsHuggingFace
from langchain.vectorstores import FAISS
from pylmkit.app import DocRAG
from pylmkit.app import WebRAG
from colorama import Fore, Back, Style

load_dotenv('.env')

# # 阿里
# os.environ["DASHSCOPE_API_KEY"] = "DASHSCOPE_API_KEY"
# llm_model = ChatTongyi(
# llm_model = ChatTongyi(model='qwen2-1.5b-instruct'
llm_model = ChatTongyi(model='qwen-max'
# llm_model = ChatTongyi(model='qwen-turbo'
#                        , streaming=True
                       )
# embed_model = EmbeddingsHuggingFace(model_name="../models/all-MiniLM-L6-v2")
embed_model = EmbeddingsHuggingFace(model_name="../models/average_word_embeddings_glove.840B.300d")
vdb_model = FAISS

with open('../res/raw_data - utf-8.csv', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

with open('../res/rag_data.txt', 'w', encoding='utf-8', errors='replace') as f:
    f.write(content)

loader = DocumentLoader(path='../res/rag_data.txt')
docs = loader.split(chunk_size=1000, chunk_overlap=200)

role_template = f'你是北京师范大学的问答AI，你的名字是"京师大福"，与你对话的人是北师大的学生，你的工作是为北师大的师生解决实际问题，你要按照你已经知道的信息为北师大学生详细、准确地提供相关信息。每次对话之前你都要介绍一下你自己，并表示很乐意为你的对话者服务。对话中可能需要以下辅助信息，请选择性地使用：今天是{time.strftime("%Y年%m月%d日", time.localtime())}；对话中的今年都是指的2024年。'
prompt_list = [role_template]
memory = MemoryHistoryLength(memory_length=500
                             , streamlit_web=True
                             )
rag = DocRAG(
    embed_model=embed_model,
    vdb_model=vdb_model,
    llm_model=llm_model,
    corpus=docs,
    memory=memory,
    show_language='中文',
    prompt_list=prompt_list,
    online_search_kwargs={}
)

os.system('cls')
while True:

    query = input(Fore.LIGHTYELLOW_EX + "输入你的问题：" + Fore.RESET)
    res,ref = rag.stream(query
                     # , topk=10
                     )
    print(Fore.LIGHTWHITE_EX+"[京师大福]:"+Fore.RESET)
    for i in res:
        print(i, end='')
    print()

# 今年是建校多少周年
# 毕业生要注意哪些问题

