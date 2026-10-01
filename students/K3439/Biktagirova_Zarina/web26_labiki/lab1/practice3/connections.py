import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_ADMIN")

print(db_url)