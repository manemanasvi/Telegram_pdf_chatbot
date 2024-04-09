import os 
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
OPEN_API_KEY=os.getenv('OPEN_API_KEY')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')