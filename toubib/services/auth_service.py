import os
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from fastapi_sqla import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from toubib.exceptions.exceptions import EntityNotFoundError, UnauthorizedException
from toubib.models.entities.auth import AuthSession
from toubib.models.entities.user import UserIn
from toubib.models.schemas.user import User
from toubib.services import user_service
from toubib.services.user_service import get_user_by_email

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> AuthSession:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise JWTError("Invalid token")
        return AuthSession(email=email)
    except JWTError as e:
        raise ValueError("Invalid token")

def login(data: UserIn, session: Session):
    user = get_user_by_email(data.email, session)
    if user is None:
        raise EntityNotFoundError(entity_id=str(data.email), entity_type=User)
    if not verify_password(data.password, user.password):
        raise UnauthorizedException("Invalid credentials")
    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def create(data: UserIn, session: Session):
    data.password = get_password_hash(data.password)
    return user_service.create(data, session)