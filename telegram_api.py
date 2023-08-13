from telegram import Bot
# from telegram.ext import Updater
# from telegram.error import TelegramError

from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv('.env'))

bot_token = config('BOT_TOKEN')
channlel_name = config('CHANNEL_NAME')

bot = Bot(token=bot_token)
