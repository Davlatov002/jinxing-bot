from django.core.management.base import BaseCommand
import os
from dotenv import load_dotenv
import telebot
from telebot import types
from user.models import User

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}
shopping_cart = {}
user_message_ids = {}
admin_id = "5867186069"


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    user_exists = User.objects.filter(user_telegram_id=user_id).first()

    if not user_exists:
        bot.send_message(user_id, "Ismingizni kiriting: ")
        bot.register_next_step_handler(message, get_user_info)
    elif user_exists.is_superuser:
        pass
        print("siz super adminsiz")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxinguz.netlify.app")
        buttons = [
            types.InlineKeyboardButton("🛒 Mahsulotlar", web_app=web_app_info),
            types.InlineKeyboardButton(" 📞 Bog'lanish", callback_data='support'),
        ]
        keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum! Tanlang:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    user_id = call.from_user.id

    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        print("Xabar o‘chirishda xatolik:", e)

    if call.data == 'support':
        menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
        menu_keyboard.add(types.InlineKeyboardButton('⬅️ orqaga', callback_data="orqaga"))
        bot.send_message(user_id, "Aloqa uchun:\n 📞 +998999774977 ; \nT/g: @davlatov02 ; \n Manzil https://www.google.com/maps/place//@41.00921,71.667123,15z/data=!4m6!1m5!3m4!2zNDHCsDAwJzMzLjIiTiA3McKwNDAnMDEuNiJF!8m2!3d41.00921!4d71.667123?hl=ru-RU&entry=ttu&g_ep=EgoyMDI1MDYwNC4wIKXMDSoASAFQAw%3D%3D ", reply_markup=menu_keyboard)

    elif call.data == 'orqaga':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxinguz.netlify.app")
        buttons = [
            types.InlineKeyboardButton("🛒 Mahsulotlar", web_app=web_app_info),
            types.InlineKeyboardButton(" 📞 Bog'lanish", callback_data='support'),
        ]
        keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum. Tanlang:", reply_markup=keyboard)


def get_user_info(message):
    user_id = message.from_user.id
    user_data[user_id] = {'name': message.text}

    bot.send_message(user_id, "Telefon raqamingizni yuboring (+998991234567 shunday ko'rinishda):")
    bot.register_next_step_handler(message, get_user_phone)

def get_user_phone(message):
    user_id = message.from_user.id

    data = user_data.get(user_id)
    if len(message.text) == 13 and message.text[:4] == "+998":
        if data:
            user = User.objects.create(
                user_telegram_id=user_id,
                first_name=data['name'],
                last_name=message.from_user.first_name,
                telegram_username=message.from_user.username,
                phone_number=message.text,
                username=user_id
            )
            user.save()
            bot.send_message(message.chat.id, "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            web_app_info = types.WebAppInfo(url="https://jinxinguz.netlify.app")
            buttons = [
                types.InlineKeyboardButton("🛒 Mahsulotlar", web_app=web_app_info),
                types.InlineKeyboardButton(" 📞 Bog'lanish", callback_data='support'),
            ]
            keyboard.add(*buttons)
            bot.send_message(user_id, "Assalomu alaykum! Tanlang:", reply_markup=keyboard)
            user_data.pop(user_id)
        else:
            bot.send_message(message.chat.id, "⚠️ Avval /start buyrug'ini yuboring.")
    else:
        bot.send_message(user_id, "Telefon raqamingizni xato yubordingiz qaytadan yuboring⁉️")
        bot.register_next_step_handler(message, get_user_phone)


class Command(BaseCommand):
    help = 'Telegram botni ishga tushuradi'

    def handle(self, *args, **kwargs):
        print("Bot ishga tushdi...")
        bot.infinity_polling()