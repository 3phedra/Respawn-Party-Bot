import os

from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv('DISCORD_BOT_TOKEN')
PREFIX: str = os.getenv('DISCORD_PREFIX')

if not TOKEN:
    raise ValueError('Token not found')

if not PREFIX:
    PREFIX: str = "!"

intents: Intents = Intents.default()
intents.message_content: bool = True

