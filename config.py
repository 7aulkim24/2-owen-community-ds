import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 쿠키 보안 (환경별)
    COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() == "true"
    # 로컬: False (HTTP에서도 작동)
    # 배포: True (HTTPS만 작동)

    COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")
    # 로컬: "lax" (같은 도메인 내 cross-site 요청 허용)
    # 배포: "strict" (같은 도메인 요청만 허용)

    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "86400"))  # 24시간

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()