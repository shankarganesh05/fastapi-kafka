import jwt
from datetime import datetime,timedelta

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
DELTA_EXPIRY = 60
def create_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=DELTA_EXPIRY)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token