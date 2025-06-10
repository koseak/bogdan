import asyncio
import logging
from aiogram import Dispatcher
from aiogram.exceptions import TelegramNetworkError
from core.init_bot import bot
from components.handlers.user_handlers import router as user_router
from components.handlers.admin_handlers import admin_router
from components.payment_system.payment_handlers import router as payment_router
from database.init_database import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Инициализация базы данных
        logger.info("Инициализация базы данных...")
        await init_db()
        logger.info("База данных успешно инициализирована")

        # Инициализация диспетчера
        dp = Dispatcher()
        dp.include_routers(admin_router, payment_router, user_router)
        logger.info("Маршрутизаторы подключены")

        # Удаление вебхука и запуск поллинга
        logger.info("Удаление вебхука...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Запуск поллинга...")
        await dp.start_polling(bot)
    except TelegramNetworkError as e:
        logger.error(f"Ошибка сети Telegram: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())