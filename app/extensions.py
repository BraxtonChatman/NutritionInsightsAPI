from app.config import Config
from app.clients.usda_client import USDAClient

usda_client = USDAClient(Config.USDA_API_KEY)