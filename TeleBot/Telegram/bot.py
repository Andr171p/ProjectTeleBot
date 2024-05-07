import telebot
from telebot import types
import time
from TeleBot.Telegram.config import bot_token
from TeleBot.GigaChat.model.giga_chat import GigaChatBot
from langchain.memory import ConversationBufferMemory
from TeleBot.GigaChat.prompt.template import prompt_text


user_conversation = {}

# create telegram bot:
bot = telebot.TeleBot(bot_token)

# create giga bot:
giga_chat = GigaChatBot()
giga_chat.create_giga_model()
giga_chat.add_prompt(
    file_path=r"C:\Users\andre\ProjectTeleBot\TeleBot\GigaChat\prompt\system\system.txt"
)


@bot.message_handler(content_types=['audio', 'video', 'document', 'photo'])
def not_text(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Я работаю только с текстовыми сообщениями")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    redactor_btn = types.KeyboardButton("текстовый редактор")
    smm_btn = types.KeyboardButton("smm")
    markup.add(redactor_btn, smm_btn)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для редактирования и генерации текста".format(
                         message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_answer_message(message):

    user_id = message.chat.id
    if user_id not in user_conversation:
        user_conversation[user_id] = ConversationBufferMemory()

    giga_chat.conversation.memory = user_conversation[user_id]

    user_prompts_history = [prompt_text(
        file_path=r"C:\Users\andre\ProjectTeleBot\TeleBot\GigaChat\prompt\user\redactor.txt"
    )]

    response = giga_chat.giga_answer(user_text=f"{user_prompts_history[-1]} {message.text}")
    bot.send_message(user_id, giga_chat.conversation.memory.chat_memory.messages[-1].content)
    time.sleep(2)


bot.polling(none_stop=True)

