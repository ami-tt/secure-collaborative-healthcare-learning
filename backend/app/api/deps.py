from typing import List, Optional

from fastapi import Depends, HTTPException, status, Request

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.core.security import decode_access_token

from app.models.user import User, UserRole



security_scheme = HTTPBearer(auto_error=False)





def get_client_ip(request: Request) -> str:

    """Extract client IP address, respecting reverse proxy headers."""

    forwarded = request.headers.get("X-Forwarded-For")

    if forwarded:

        return forwarded.split(",")[0].strip()

    return request.client.host if request.client else "127.0.0.1"





def get_current_user(

    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),

    db: Session = Depends(get_db)

) -> User:

    """

    Validate the incoming JWT Bearer token and retrieve the corresponding active user.

    """

    if not credentials or not credentials.credentials:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Authentication credentials were not provided.",

            headers={"WWW-Authenticate": "Bearer"},

        )



    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid or expired authentication token.",

            headers={"WWW-Authenticate": "Bearer"},

        )



    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token payload missing subject identifier.",

            headers={"WWW-Authenticate": "Bearer"},

        )



    user = db.query(User).filter(User.id == user_id).first()

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="User account associated with this token no longer exists.",

            headers={"WWW-Authenticate": "Bearer"},

        )



    if not user.is_active:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="User account has been deactivated. Contact an administrator.",

        )



    return user





def require_roles(allowed_roles: List[UserRole]):

    """

    Role-Based Access Control (RBAC) dependency factory.

    Enforces that current authenticated user belongs to at least one allowed role.

    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:

        if current_user.role not in allowed_roles:

            role_names = [r.value for r in allowed_roles]

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail=f"Access denied. Required role in: {role_names}. Current role: {current_user.role.value}.",

            )

        return current_user



    return role_checker
