import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import BotHandlers


class TelegramBot:
    def __init__(self, config, rag_config):
        self.application = Application.builder().token(config.telegram_token).build()
        self.handlers = BotHandlers(rag_config)
        self._register_handlers()

    async def start_processing(self):
        # Запускаем задачу обработки очереди только после старта приложения
        asyncio.create_task(self.handlers.process_queue())

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message))

    def run(self):
        # asyncio.run(self.start_processing())
        loop = asyncio.get_event_loop()
        loop.create_task(self.start_processing())
        self.application.run_polling()
