import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")

def validate_config():
    if Config.USDA_API_KEY == "DEMO_KEY":
        print("WARNING: Using USDA demo API key")