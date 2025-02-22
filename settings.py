import os

from dotenv import load_dotenv

load_dotenv(".env.local")

valid_email = os.getenv("valid_email")
valid_password = os.getenv("valid_password")
