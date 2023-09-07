from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from sending_app.models import TelegramUser

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = TelegramUser.objects.filter(user_id=user_id, chat_id=chat_id)
    if user:
        bot.send_message(chat_id, f"Вы уже подписаны на уведомления! Ваш id {user_id}.")
    else:
        TelegramUser.objects.create(user_id=user_id, chat_id=chat_id)
        bot.send_message(chat_id, f"Вы успешно подписались на уведомления!\nВаш id {user_id}. Вставьте его в личном кабинете в графе 'telegram_given_id' чтобы привязать ваш аккаунт к данному чату.")


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, это ваш бот! Введите /subscribe чтобы подписаться на канал!")


@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    bot.reply_to(message, "Извините, я не понимаю эту команду. Пожалуйста, воспользуйтесь доступными командами.")



