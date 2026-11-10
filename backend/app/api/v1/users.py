from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.models.user import User, UserRole

from app.schemas.user import UserResponse, UserUpdate, UserDetailResponse

from app.api.deps import get_current_user, require_roles, get_client_ip

from app.services.audit_service import AuditService



router = APIRouter()





@router.get(

    "/",

    response_model=List[UserResponse],

    summary="List users (Admin only)"

)

def list_users(

    skip: int = Query(0, ge=0),

    limit: int = Query(50, ge=1, le=100),

    role: Optional[UserRole] = None,

    current_user: User = Depends(require_roles([UserRole.ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Retrieve paginated list of platform users. Restricted strictly to System Administrators.

    """

    query = db.query(User)

    if role:

        query = query.filter(User.role == role)

    return query.offset(skip).limit(limit).all()





@router.get(

    "/{user_id}",

    response_model=UserDetailResponse,

    summary="Get user details by ID"

)

def get_user_by_id(

    user_id: str,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    Retrieve user details by ID. Non-admin users may only view their own user profile.

    """

    if current_user.role != UserRole.ADMIN and current_user.id != user_id:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="You are not authorized to view this user's profile."

        )



    user = db.query(User).filter(User.id == user_id).first()

    if not user:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"User with ID '{user_id}' was not found."

        )

    return user





@router.patch(

    "/{user_id}",

    response_model=UserResponse,

    summary="Update user profile or status (Admin or Self)"

)

def update_user(

    user_id: str,

    user_update: UserUpdate,

    request: Request,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    Update user profile attributes. Role, verification, and active status modifications require Admin privileges.

    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"User with ID '{user_id}' was not found."

        )



    is_admin = (current_user.role == UserRole.ADMIN)

    if not is_admin and current_user.id != user_id:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="You are not permitted to modify this user account."

        )



    # Non-admins cannot alter roles or verification flags

    if not is_admin and (user_update.role is not None or user_update.is_active is not None or user_update.is_verified is not None):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Administrative privileges are required to change roles or account status."

        )



    update_dict = user_update.model_dump(exclude_unset=True)

    for field, value in update_dict.items():

        setattr(user, field, value)



    db.commit()

    db.refresh(user)



    AuditService.log(

        db,

        action="USER_UPDATE",

        resource_type="USER",

        resource_id=user.id,

        user_id=current_user.id,

        institution_id=user.institution_id,

        ip_address=get_client_ip(request),

        details=update_dict,

        status="SUCCESS"

    )



    return user
