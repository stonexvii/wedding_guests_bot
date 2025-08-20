import dotenv
import os
# from classes import FileManager

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))
# MONITOR_TG_ID = 0
# MONITOR_TG_ID = int(os.getenv('MONITOR_TG_ID'))

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

PUSHER_APP_ID = os.getenv('PUSHER_APP_ID')
PUSHER_KEY = os.getenv('PUSHER_KEY')
PUSHER_SECRET = os.getenv('PUSHER_SECRET')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')

# INTRO_MESSAGE = FileManager.read('intro')
# CAP_MESSAGE = FileManager.read('cap')
