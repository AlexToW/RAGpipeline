import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from rag.pipeline import RAGPipeline


class BotHandlers:
    def __init__(self, rag_config):
        self.rag_pipeline = RAGPipeline(rag_config)

        self.greeting_message = """
        👋 Привет! Я ваш помощник по продуктам KATA EDR.

        💡 Задайте мне вопрос о документации, и я найду нужную информацию!

        ❔ Начните с вопроса, например: "Сколько серверов минимально необходимо при кластерной установке?"
        """
        # self.processing_task = asyncio.create_task(self.process_queue())
        self.message_queue = asyncio.Queue()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.greeting_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        # Добавляем сообщение в очередь вместе с контекстом
        await self.message_queue.put((update.message.chat_id, user_message, context))


    async def process_queue(self):
        while True:
            # Получаем сообщение из очереди
            chat_id, user_message, context = await self.message_queue.get()
            response = self.rag_pipeline.get_response(user_message)
            await context.bot.send_message(chat_id=chat_id, text=response)
            await asyncio.sleep(3)  # 1 секунда интервал

    # async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     user_message = update.message.text
    #     response = self.rag_pipeline.get_response(user_message)
    #     await update.message.reply_text(response)


