from dotenv import load_dotenv
import os

load_dotenv()

TG_BOT_TOKEN=os.environ["TG_BOT_TOKEN"]
MONGO_URI=os.environ["MONGO_URI"]
HF_TOKEN=os.environ["HF_TOKEN"]