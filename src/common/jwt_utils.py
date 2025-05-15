import os

from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

from src.application.domain.model.user import User

load_dotenv(dotenv_path="dev.env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "1tnz2B8JoznGVBFInnExFC7CYe5l-P45H1CgHFoWIAE")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")


def create_jwt_token(user: User) -> str:
    to_encode = {
        "sub": str(user.id),
        "email": str(user.email),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
