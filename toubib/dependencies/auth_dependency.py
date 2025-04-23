from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqla import Session

from toubib.exceptions.exceptions import EntityNotFoundError, UnauthorizedException
from toubib.models.schemas.user import User
from toubib.services.auth_service import decode_access_token
from toubib.services.user_service import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends()):
    try:
        token_data = decode_access_token(token)
        user = get_user_by_email(token_data.email, session)
        if user is None:
            raise EntityNotFoundError(entity_id=str(token_data.email), entity_type=User)
        return user
    except ValueError as e:
        raise UnauthorizedException("Invalid token")
