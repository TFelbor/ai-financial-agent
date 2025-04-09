import os
from dotenv import load_dotenv

load_dotenv('config/secrets.env')

class Config:
    CACHE_DIR = os.path.join(os.path.dirname(__file__), '../../data/cache')
    YAHOO_API = os.getenv('YAHOO_API_TOKEN')
    GLASSNODE_API = os.getenv('GLASSNODE_API_KEY')