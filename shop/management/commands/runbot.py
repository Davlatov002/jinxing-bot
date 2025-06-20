from django.core.management.base import BaseCommand
import os

from django.urls import exceptions
from dotenv import load_dotenv
import telebot
from telebot import types

from user.models import User

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}
user_message_ids = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    user_exists = User.objects.filter(user_telegram_id=user_id).first()

    if not user_exists:
        bot.send_message(user_id, "Ismingizni kiriting: ")
        bot.register_next_step_handler(message, get_user_info)
    elif user_exists.is_superuser:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxingbot.uz/")
        buttons = [
            types.InlineKeyboardButton("🔥 Bosh menyu", web_app=web_app_info),
        ]
        keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum!", reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxingbot.uz/")
        buttons = [
            types.InlineKeyboardButton("🔥 Mahsulotlar", web_app=web_app_info),
            types.InlineKeyboardButton("👤 Siz haqingizda", callback_data='user'),
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
        message_text = (
            "📞 <b>Aloqa uchun ma'lumotlar:</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📱 <b>Telefon:</b> +998999774977\n"
            "📱 <b>Telefon:</b> +998770677717\n"
            "💬 <b>Telegram:</b> <a href='https://t.me/Umarhon999774977'>@Umarhon999774977</a>\n\n"
            "📍 <b>Manzil:</b>\n"
            "<a href='https://www.google.com/maps/place//@41.00921,71.667123,15z'>📌 Xaritada ko‘rish (Google Maps)</a>\n"
            "━━━━━━━━━━━━━━━━━━"
        )

        bot.send_message(
            user_id,
            message_text,
            reply_markup=menu_keyboard,
            parse_mode="HTML"
        )

    elif call.data == 'orqaga':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxingbot.uz/")
        buttons = [
            types.InlineKeyboardButton("🔥 Mahsulotlar", web_app=web_app_info),
            types.InlineKeyboardButton("👤 Siz haqingizda", callback_data='user'),
            types.InlineKeyboardButton(" 📞 Bog'lanish", callback_data='support'),
        ]
        keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum. Tanlang:", reply_markup=keyboard)
    elif call.data == 'user':
        user = User.objects.filter(user_telegram_id=user_id).first()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton("🔄 Malumotlarni yangilash", callback_data="update_info"),
            types.InlineKeyboardButton('⬅️ Orqaga', callback_data="orqaga"),
        ]
        keyboard.add(*buttons)
        bot.send_message(user_id, f"Isim: {user.first_name} \nTelefon raqam: {user.phone_number} ", reply_markup=keyboard)
    elif call.data == 'update_info':
        bot.send_message(user_id, "Ismingizni kiriting: ")
        bot.register_next_step_handler(call.message, get_user_info)


def send_telegram_message(message: str):
    try:
        users = User.objects.filter(is_superuser=True)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        web_app_info = types.WebAppInfo(url="https://jinxingbot.uz/")
        buttons = [
            types.InlineKeyboardButton("🔥 Bosh menyu", web_app=web_app_info),
        ]
        keyboard.add(*buttons)
        for user in users:
            try:
                bot.send_message(user.user_telegram_id, message, parse_mode="HTML", reply_markup=keyboard)
            except exceptions:
                pass
    except Exception as e:
        print(f"Telegramga habar yuborishda xatolik: {e}")


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
            user, created = User.objects.update_or_create(
                user_telegram_id=user_id,
                defaults={
                    'first_name': data['name'],
                    'last_name': message.from_user.first_name,
                    'telegram_username': message.from_user.username,
                    'phone_number': message.text,
                    'username': user_id
                }
            )
            bot.send_message(message.chat.id, "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            web_app_info = types.WebAppInfo(url="https://jinxingbot.uz/")
            buttons = [
                types.InlineKeyboardButton("🔥 Mahsulotlar", web_app=web_app_info),
                types.InlineKeyboardButton("👤 Siz haqingizda", callback_data='user'),
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