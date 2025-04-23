from fastapi_sqla import Session
from sqlalchemy.exc import IntegrityError

from toubib.exceptions.exceptions import EntityNotFoundError, IllegalStateException, DuplicateKeyException
from toubib.models.entities.user import UserIn, UserModel
from toubib.models.schemas.user import User


def create(body: UserIn, session: Session) -> UserModel:
    user = User(**body.dict())
    try:
        session.add(user)
        session.flush()
    except IntegrityError as e:
        session.rollback()
        error_message = str(e.orig).lower()
        if 'unique' in str(e.orig).lower():
            raise DuplicateKeyException(error_message, User)
        else:
            raise IllegalStateException(f"Unknown error creating user: {str(e)}", e)
    return UserModel.from_orm(user)

def get_user_by_email(email: str, session: Session) -> User:
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise EntityNotFoundError(entity_id=email, entity_type=User)
    return user
