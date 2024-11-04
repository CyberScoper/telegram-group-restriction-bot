import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import logging
from datetime import datetime, timedelta
import nest_asyncio
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Попробуйте использовать DEBUG для большего количества информации
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Словарь для отслеживания задач пользователей
user_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    await update.message.reply_text('Бот запущен и готов к работе!')

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Новый участник добавлен: {update.message.new_chat_members}")
    for member in update.message.new_chat_members:
        # Запускаем задачу на 8 минут
        task = asyncio.create_task(
            restrict_user_after_delay(
                update.effective_chat.id, member.id, context
            )
        )
        # Сохраняем задачу, чтобы иметь возможность управлять ею позже
        logger.info(f"Создана задача для ограничения пользователя: {member.id}")
        user_tasks[member.id] = task

async def restrict_user_after_delay(chat_id, user_id, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Запуск ограничения для пользователя {user_id} через 7 минут")
    # Ждем 7 минут
    await asyncio.sleep(7 * 60)  # Реальное время ожидания 7 минут
    logger.info(f"Попытка ограничения пользователя {user_id} на 12 часов")

    try:
        # Получаем информацию о пользователе для проверки его статуса в чате
        user = await context.bot.get_chat_member(chat_id, user_id)
        if user.status in ['left', 'kicked']:
            logger.info(f"Пользователь {user_id} уже покинул чат, ограничение не будет применено.")
            return

        # Ограничиваем пользователя на 12 часов
        permissions = ChatPermissions(can_send_messages=False)
        until_date = datetime.utcnow() + timedelta(hours=12)  # Ограничение на 12 часов
        await context.bot.restrict_chat_member(
            chat_id, user_id, permissions=permissions, until_date=until_date
        )
        logger.info(f"Пользователь {user_id} успешно ограничен на 12 часов")

        # Запускаем задачу для отправки сообщения через 12 часов
        asyncio.create_task(schedule_welcome_message(chat_id, user_id, context))
    except Exception as e:
        logger.error(f"Ошибка при ограничении пользователя {user_id}: {e}")


def mention_html(user):
    if user.username:
        return f"@{user.username}"
    else:
        return f"{user.first_name}"

async def schedule_welcome_message(chat_id, user_id, context: ContextTypes.DEFAULT_TYPE):
    # Ждем 12 часов (время ограничения)
    await asyncio.sleep(12 * 60 * 60)  # Ожидание 12 часов перед отправкой сообщения

    try:
        # Получаем информацию о пользователе для проверки статуса
        user = await context.bot.get_chat_member(chat_id, user_id)

        # Проверяем, что пользователь все еще в чате
        if user.status not in ['left', 'kicked']:
            # Формируем сообщение с упоминанием имени пользователя
            username = mention_html(user.user)

            # Отправляем приветственное сообщение
            await context.bot.send_message(
                chat_id,
                f"Привет, {username}. Будем рады фотке твоего велика.",
                parse_mode='HTML',
            )
            logger.info(f"Приветственное сообщение отправлено пользователю {user_id}")
        else:
            logger.info(f"Пользователь {user_id} покинул чат, сообщение не отправлено.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения для пользователя {user_id}: {e}")

async def main():

    application = ApplicationBuilder().token("OUR API FROM PAPA BOT").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member)
    )

    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    try:
        
        loop = asyncio.get_running_loop()
        
        loop.create_task(main())
        loop.run_forever()
    except RuntimeError:
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

