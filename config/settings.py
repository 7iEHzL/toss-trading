import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def parse_env_bool(value):
    return isinstance(value, str) and value.strip().lower() == "true"


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENABLE_REAL_ORDER = parse_env_bool(os.getenv("ENABLE_REAL_ORDER"))
