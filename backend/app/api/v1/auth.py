from datetime import datetime, timezone
import logging

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.models.user import User, UserRole
from app.models.institution import Institution
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserDetailResponse,
)
from app.api.deps import get_current_user, get_client_ip
from app.services.audit_service import AuditService


router = APIRouter()

logger = logging.getLogger(__name__)


# ============================================================
# USER REGISTRATION
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new researcher account",
)
def register_user(
    user_in: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public registration endpoint.

    All publicly registered accounts receive the RESEARCHER role.
    Administrative roles must be provisioned through a trusted
    administrative process.
    """

    client_ip = get_client_ip(request)

    email_clean = str(user_in.email).lower().strip()

    # Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == email_clean)
        .first()
    )

    if existing_user:

        AuditService.log(
            db,
            action="AUTH_REGISTER_FAILED",
            resource_type="USER",
            ip_address=client_ip,
            details={
                "email": email_clean,
                "reason": "Email already registered",
            },
            status="FAILED",
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address is already registered.",
        )

    # Validate institution if supplied
    if user_in.institution_id:

        institution = (
            db.query(Institution)
            .filter(
                Institution.id == user_in.institution_id
            )
            .first()
        )

        if not institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The specified institution was not found.",
            )

    # Hash password
    hashed_password = get_password_hash(
        user_in.password
    )

    # Public registration always creates a researcher
    user = User(
        email=email_clean,
        password_hash=hashed_password,
        full_name=user_in.full_name.strip(),
        role=UserRole.RESEARCHER,
        institution_id=user_in.institution_id,
        is_active=True,
        is_verified=True,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        logger.exception("User registration failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register the account.",
        )

    # Record successful registration
    AuditService.log(
        db,
        action="AUTH_REGISTER_SUCCESS",
        resource_type="USER",
        resource_id=user.id,
        user_id=user.id,
        institution_id=user.institution_id,
        ip_address=client_ip,
        details={
            "email": user.email,
            "role": user.role.value,
        },
        status="SUCCESS",
    )

    return user


# ============================================================
# USER LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate and receive JWT token",
)
def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Authenticate an existing user and generate a JWT access token.
    """

    client_ip = get_client_ip(request)

    email_clean = str(
        login_data.email
    ).lower().strip()

    user = (
        db.query(User)
        .filter(User.email == email_clean)
        .first()
    )

    # Verify credentials
    if (
        not user
        or not verify_password(
            login_data.password,
            user.password_hash,
        )
    ):

        AuditService.log(
            db,
            action="AUTH_LOGIN_FAILED",
            resource_type="USER",
            ip_address=client_ip,
            details={
                "email": email_clean,
                "reason": "Invalid credentials",
            },
            status="FAILED",
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check account status
    if not user.is_active:

        AuditService.log(
            db,
            action="AUTH_LOGIN_BLOCKED",
            resource_type="USER",
            resource_id=user.id,
            user_id=user.id,
            ip_address=client_ip,
            details={
                "email": email_clean,
                "reason": "Account deactivated",
            },
            status="UNAUTHORIZED",
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated. Please contact an administrator.",
        )

    # Update last login
    user.last_login = datetime.now(timezone.utc)

    try:
        db.commit()

    except Exception:
        db.rollback()
        logger.exception("Login timestamp update failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete login.",
        )

    # Generate JWT token
    access_token = create_access_token(
        subject=user.id,
        role=user.role.value,
        institution_id=user.institution_id,
    )

    # Record successful login
    AuditService.log(
        db,
        action="AUTH_LOGIN_SUCCESS",
        resource_type="USER",
        resource_id=user.id,
        user_id=user.id,
        institution_id=user.institution_id,
        ip_address=client_ip,
        details={
            "role": user.role.value,
        },
        status="SUCCESS",
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role.value,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        institution_id=user.institution_id,
    )


# ============================================================
# CURRENT USER PROFILE
# ============================================================

@router.get(
    "/me",
    response_model=UserDetailResponse,
    summary="Get current authenticated user profile",
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Return details of the currently authenticated user.
    """

    return current_user
