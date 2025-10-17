from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime, random, pytz

# ================= Настройки =================
TOKEN = "8366342998:AAHE49-3UoAjBZTsEqikKZtnUa_JWgvs1-g"  # вставь свой токен
GIRL_ID = 388657962                                    # ID девушки
TZ = pytz.timezone("Europe/Moscow")                   # таймзона через pytz

# ================= Сообщения-напоминания =================
REMINDER_MESSAGES = [
    "Мяу~ ❤️ не забудь таблеточку, моя хорошая!",
    "Твоя пушистая мурлыка шепчет: пора таблеточку 💊",
    "Мур-мур~ 😽 заботься о себе, котёнок!",
    "Мурлыкает рядом: не забудь таблеточку, солнце 💕"
]

# ================= Функция отправки напоминания =================
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(REMINDER_MESSAGES)
    try:
        await context.bot.send_message(chat_id=GIRL_ID, text=message)
        print("✅ Сообщение отправлено!")
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")

# ================= Команда /start =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Мяу! 😺 Я буду напоминать тебе пить таблеточку каждый день 💊")

    # Удаляем старые задачи, если есть
    for job in context.job_queue.get_jobs_by_name(str(chat_id)):
        job.schedule_removal()
        print("🧹 Старые задачи удалены")

    # Время ежедневного напоминания с pytz
    run_time = datetime.time(hour=22, minute=0, tzinfo=TZ)

    # Создаём новую задачу
    context.job_queue.run_daily(
        send_reminder,
        time=run_time,
        name=str(chat_id)
    )
    print(f"✅ Новая задача запланирована на {run_time.strftime('%H:%M:%S')} (местное время)")

# ================= Основной запуск =================
def main():
    print("🚀 Запускаю бота…")

    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчик команды
    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
