import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
STATIC_DIR = ROOT_DIR / 'static'

DEV_ENV_FILEPATH = ROOT_DIR / '.env'
TEST_ENV_FILEPATH = ROOT_DIR / '.test.env'

ENV = os.environ.get('ENV')

if ENV == 'dev':
    load_dotenv(DEV_ENV_FILEPATH)
elif ENV == 'test':
    load_dotenv(TEST_ENV_FILEPATH)


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_PASS = os.environ.get("DB_PASS")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
SECRET = os.environ.get("SECRET")



