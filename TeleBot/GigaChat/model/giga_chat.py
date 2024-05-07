from TeleBot.GigaChat.model.auth_data import client_id, client_secret
from langchain.chat_models.gigachat import GigaChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
import base64
from TeleBot.GigaChat.prompt.template import prompt_text


class GigaChatBot:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.giga_api = None
        self.llm = None
        self.conversation = None

    def get_giga_api(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        self.giga_api = encoded_credentials

    def create_giga_model(self):
        self.get_giga_api()
        llm = GigaChat(credentials=self.giga_api,
                       verify_ssl_certs=False)
        conversation = ConversationChain(llm=llm,
                                         verbose=False,
                                         memory=ConversationBufferMemory(llm=llm))

        self.llm = llm
        self.conversation = conversation

    def add_prompt(self, file_path):
        template = prompt_text(file_path=file_path)
        self.conversation.prompt.template = template

    def giga_answer(self, user_text):
        return self.conversation.predict(input=user_text)

