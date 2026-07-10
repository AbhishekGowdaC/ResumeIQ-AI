from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from app.auth.jwt_handler import verify_access_token

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme)

):
    payload = verify_access_token(token)
    return payload