import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальные переменные
scheduler = BackgroundScheduler()
scheduler.start()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот для напоминаний. Используй /addreminder чтобы добавить напоминание.")

# Команда /addreminder
def add_reminder(update: Update, context: CallbackContext) -> None:
    try:
        # Ожидаем формат: /addreminder <время> <текст>
        args = context.args
        if len(args) < 2:
            update.message.reply_text("Используй формат: /addreminder <время в формате ГГГГ-ММ-ДД ЧЧ:ММ> <текст>")
            return

        time_str = f"{args[0]} {args[1]}"
        text = " ".join(args[2:])
        reminder_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        # Добавляем задачу в планировщик
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=reminder_time,
            args=[update.message.chat_id, text]
        )

        update.message.reply_text(f"Напоминание добавлено на {reminder_time}!")
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

# Функция для отправки напоминания
def send_reminder(chat_id: int, text: str) -> None:
    context.bot.send_message(chat_id=chat_id, text=f"⏰ Напоминание: {text}")

# Основная функция
def main() -> None:
    # Токен бота (замени на свой)
    TOKEN = '7574484073:AAHsoPlwtWzkEMoAYbF9iWL-Q-AY3RyWk3w'

    # Создаем Updater и передаем ему токен
    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("addreminder", add_reminder))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()