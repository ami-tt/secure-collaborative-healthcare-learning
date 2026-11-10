from datetime import datetime, timedelta, timezone

from typing import Any, Dict, Optional, Union

import bcrypt

from jose import JWTError, jwt

from app.core.config import settings





def verify_password(plain_password: str, hashed_password: str) -> bool:

    """

    Verify a plaintext password against a stored bcrypt hash.

    Safely encodes both to UTF-8 and handles max bcrypt byte lengths.

    """

    if not plain_password or not hashed_password:

        return False

    try:

        # bcrypt handles max 72 bytes; truncate safely to prevent crash

        plain_bytes = plain_password.encode("utf-8")[:72]

        hash_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_bytes, hash_bytes)

    except Exception:

        return False





def get_password_hash(password: str) -> str:

    """

    Hash a password using bcrypt with a randomized salt (work factor = 12).

    """

    plain_bytes = password.encode("utf-8")[:72]

    salt = bcrypt.gensalt(rounds=12)

    hashed = bcrypt.hashpw(plain_bytes, salt)

    return hashed.decode("utf-8")





def create_access_token(

    subject: Union[str, Any],

    role: str,

    institution_id: Optional[str] = None,

    expires_delta: Optional[timedelta] = None

) -> str:

    """

    Generate a signed JWT access token containing subject (user_id), email, role, and expiration.

    """

    if expires_delta:

        expire = datetime.now(timezone.utc) + expires_delta

    else:

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)



    to_encode: Dict[str, Any] = {

        "sub": str(subject),

        "role": role,

        "institution_id": str(institution_id) if institution_id else None,

        "exp": expire,

        "iat": datetime.now(timezone.utc)

    }



    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt





def decode_access_token(token: str) -> Optional[Dict[str, Any]]:

    """

    Decode and validate a signed JWT token. Returns payload dict or None if invalid/expired.

    """

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]

        )

        return payload

    except JWTError:

        return None
