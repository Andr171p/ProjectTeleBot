from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
import base64
from langchain.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain_community.embeddings import GigaChatEmbeddings

from TeleBot.GigaChat.model.auth_data import client_id, client_secret


def get_giga_api():
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return encoded_credentials


token = get_giga_api()
print(token)

llm = GigaChat(credentials=token, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

'''question = "Какой плащ был у Понтия Пилата?"
print(llm([HumanMessage(content=question)]).content)'''

loader = TextLoader("StranaDevelopment.txt", encoding='UTF-8')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
documents = text_splitter.split_documents(documents)
print(f"Total documents: {len(documents)}")

embeddings = GigaChatEmbeddings(
    credentials=token, verify_ssl_certs=False
)

db = Chroma.from_documents(
    documents,
    embeddings,
    client_settings=Settings(anonymized_telemetry=False)
)
