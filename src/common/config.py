import os

from dotenv import load_dotenv

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password

load_dotenv(dotenv_path="dev.env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "1tnz2B8JoznGVBFInnExFC7CYe5l-P45H1CgHFoWIAE")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
DUMMY_EMAIL = os.getenv(
    "DUMMY_EMAIL", "OXvgLutyHveL7_veyNhFDf1fy6ERNP5uJBQrLMzZ2sU@example.com"
)
DUMMY_USER = User(
    id=UserId(1),
    name=Name("foo"),
    email=Email(DUMMY_EMAIL),
    password=Password("secret"),
    address=Address(
        street_name="bar",
        street_number=42,
        city="baz",
        postal_code="qux",
        country="tar",
    ),
    status=Status.enable(),
)
