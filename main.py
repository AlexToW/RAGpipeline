from bot.telegram_bot import TelegramBot
from config import Config, RAGConfig
import yaml
import os
from logger import logger


if __name__ == "__main__":

    with open('credentials.yaml', 'r') as file:
        creds = yaml.load(file, Loader=yaml.FullLoader)

    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = creds["mistral_api_key"]


    config = Config(telegram_token=creds["telegram_token"], mistral_api_key=creds["mistral_api_key"])
    rag_config = RAGConfig()
    bot = TelegramBot(config, rag_config)
    bot.run()
