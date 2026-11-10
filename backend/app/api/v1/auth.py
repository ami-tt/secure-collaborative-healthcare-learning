from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.core.security import verify_password, get_password_hash, create_access_token

from app.models.user import User, UserRole

from app.models.institution import Institution

from app.schemas.auth import LoginRequest, Token

from app.schemas.user import UserCreate, UserResponse, UserDetailResponse

from app.api.deps import get_current_user, get_client_ip

from app.services.audit_service import AuditService



router = APIRouter()





@router.post(

    "/register",

    response_model=UserResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Register a new user account"

)

def register_user(

    user_in: UserCreate,

    request: Request,

    db: Session = Depends(get_db)

):

    """

    Register a new platform user with specified role (Researcher, Hospital Administrator, or Admin).

    Verifies institutional affiliation if provided and hashes the password securely.

    """

    client_ip = get_client_ip(request)



    # Check if email is already taken

    existing_user = db.query(User).filter(User.email == user_in.email.lower().strip()).first()

    if existing_user:

        AuditService.log(

            db,

            action="AUTH_REGISTER_FAILED",

            resource_type="USER",

            ip_address=client_ip,

            details={"email": user_in.email, "reason": "Email already registered"},

            status="FAILED"

        )

        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,

            detail="An account with this email address is already registered."

        )



    # If institution_id is provided, verify it exists

    if user_in.institution_id:

        institution = db.query(Institution).filter(Institution.id == user_in.institution_id).first()

        if not institution:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail=f"Affiliated institution '{user_in.institution_id}' was not found."

            )



    # Create user

    hashed_password = get_password_hash(user_in.password)

    user = User(

        email=user_in.email.lower().strip(),

        password_hash=hashed_password,

        full_name=user_in.full_name.strip(),

        role=user_in.role,

        institution_id=user_in.institution_id,

        is_active=True,

        # Auto-verify researchers for testing; admins can toggle verification

        is_verified=(user_in.role == UserRole.RESEARCHER)

    )



    db.add(user)

    db.commit()

    db.refresh(user)



    AuditService.log(

        db,

        action="AUTH_REGISTER_SUCCESS",

        resource_type="USER",

        resource_id=user.id,

        user_id=user.id,

        institution_id=user.institution_id,

        ip_address=client_ip,

        details={"email": user.email, "role": user.role.value},

        status="SUCCESS"

    )



    return user





@router.post(

    "/login",

    response_model=Token,

    summary="Authenticate and receive JWT token"

)

def login(

    login_data: LoginRequest,

    request: Request,

    db: Session = Depends(get_db)

):

    """

    Validate user credentials, record login timestamp, and issue signed JWT access token.

    """

    client_ip = get_client_ip(request)

    email_clean = login_data.email.lower().strip()



    user = db.query(User).filter(User.email == email_clean).first()

    if not user or not verify_password(login_data.password, user.password_hash):

        AuditService.log(

            db,

            action="AUTH_LOGIN_FAILED",

            resource_type="USER",

            ip_address=client_ip,

            details={"email": email_clean, "reason": "Invalid credentials"},

            status="FAILED"

        )

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Incorrect email or password.",

            headers={"WWW-Authenticate": "Bearer"},

        )



    if not user.is_active:

        AuditService.log(

            db,

            action="AUTH_LOGIN_BLOCKED",

            resource_type="USER",

            resource_id=user.id,

            user_id=user.id,

            ip_address=client_ip,

            details={"email": email_clean, "reason": "Account deactivated"},

            status="UNAUTHORIZED"

        )

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Your account has been deactivated. Please contact an administrator."

        )



    # Update last login timestamp

    user.last_login = datetime.now(timezone.utc)

    db.commit()



    # Generate JWT token

    access_token = create_access_token(

        subject=user.id,

        role=user.role.value,

        institution_id=user.institution_id

    )



    AuditService.log(

        db,

        action="AUTH_LOGIN_SUCCESS",

        resource_type="USER",

        resource_id=user.id,

        user_id=user.id,

        institution_id=user.institution_id,

        ip_address=client_ip,

        details={"role": user.role.value},

        status="SUCCESS"

    )



    return Token(

        access_token=access_token,

        token_type="bearer",

        role=user.role.value,

        user_id=user.id,

        email=user.email,

        full_name=user.full_name,

        institution_id=user.institution_id

    )





@router.get(

    "/me",

    response_model=UserDetailResponse,

    summary="Get current authenticated user profile"

)

def get_current_user_profile(

    current_user: User = Depends(get_current_user)

):

    """

    Retrieve profile details and affiliated institution for the current authenticated user.

    """

    return current_user
