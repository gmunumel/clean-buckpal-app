from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dependency_injector.wiring import inject, Provide

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.adapter.outbound.persistence.in_memory_data_user_repository import (
    InMemoryDataUserRepository,
)
from src.common.config import (
    DUMMY_EMAIL,
    DUMMY_USER,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)


SECURITY = HTTPBearer()


def create_jwt_token(user: User) -> str:
    to_encode: dict[str, str | datetime] = {
        "sub": str(user.id),
        "email": str(user.email),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@inject
def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(SECURITY),
    user_repository: InMemoryDataUserRepository = Depends(
        Provide["in_memory_data_user_repository"]
    ),
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user_email = payload.get("email")
        if user_email == DUMMY_EMAIL:
            return DUMMY_USER
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
            )
        user = user_repository.find_by_id(UserId(int(user_id)))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found."
            )
        return user
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
