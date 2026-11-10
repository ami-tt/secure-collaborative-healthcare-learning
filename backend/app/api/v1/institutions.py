import secrets

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.core.security import get_password_hash

from app.models.institution import Institution, InstitutionStatus

from app.models.user import User, UserRole

from app.schemas.institution import InstitutionCreate, InstitutionUpdate, InstitutionResponse

from app.api.deps import get_current_user, require_roles, get_client_ip

from app.services.audit_service import AuditService



router = APIRouter()





@router.get(

    "/",

    response_model=List[InstitutionResponse],

    summary="List registered institutions"

)

def list_institutions(

    skip: int = Query(0, ge=0),

    limit: int = Query(50, ge=1, le=100),

    status_filter: Optional[InstitutionStatus] = None,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    List all healthcare institutions participating in the federated network.

    """

    query = db.query(Institution)

    if status_filter:

        query = query.filter(Institution.status == status_filter)

    return query.offset(skip).limit(limit).all()





@router.post(

    "/",

    response_model=InstitutionResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Register a new healthcare institution"

)

def register_institution(

    institution_in: InstitutionCreate,

    request: Request,

    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.HOSPITAL_ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Register a new hospital or clinical institution. Generates an institutional client key.

    """

    existing = db.query(Institution).filter(

        Institution.institution_code == institution_in.institution_code.upper().strip()

    ).first()

    if existing:

        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,

            detail=f"Institution code '{institution_in.institution_code}' is already registered."

        )



    # Generate edge client API key

    raw_api_key = f"fl_inst_{secrets.token_urlsafe(32)}"

    api_key_hash = get_password_hash(raw_api_key)



    institution = Institution(

        name=institution_in.name.strip(),

        institution_code=institution_in.institution_code.upper().strip(),

        contact_email=institution_in.contact_email.lower().strip(),

        phone=institution_in.phone,

        address=institution_in.address,

        api_key_hash=api_key_hash,

        # Admin registrations are immediately active; self-registrations require admin verification

        status=InstitutionStatus.ACTIVE if current_user.role == UserRole.ADMIN else InstitutionStatus.PENDING_VERIFICATION

    )



    db.add(institution)

    db.commit()

    db.refresh(institution)



    AuditService.log(

        db,

        action="INSTITUTION_REGISTERED",

        resource_type="INSTITUTION",

        resource_id=institution.id,

        user_id=current_user.id,

        institution_id=institution.id,

        ip_address=get_client_ip(request),

        details={"code": institution.institution_code, "status": institution.status.value},

        status="SUCCESS"

    )



    return institution





@router.get(

    "/{institution_id}",

    response_model=InstitutionResponse,

    summary="Get institution details by ID"

)

def get_institution(

    institution_id: str,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    Retrieve institution details.

    """

    institution = db.query(Institution).filter(Institution.id == institution_id).first()

    if not institution:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"Institution '{institution_id}' was not found."

        )

    return institution





@router.patch(

    "/{institution_id}/status",

    response_model=InstitutionResponse,

    summary="Approve or update institution status (Admin only)"

)

def update_institution_status(

    institution_id: str,

    new_status: InstitutionStatus,

    request: Request,

    current_user: User = Depends(require_roles([UserRole.ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Verify, activate, or suspend an institution. Restricted to System Administrators.

    """

    institution = db.query(Institution).filter(Institution.id == institution_id).first()

    if not institution:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"Institution '{institution_id}' was not found."

        )



    old_status = institution.status

    institution.status = new_status

    db.commit()

    db.refresh(institution)



    AuditService.log(

        db,

        action="INSTITUTION_STATUS_CHANGE",

        resource_type="INSTITUTION",

        resource_id=institution.id,

        user_id=current_user.id,

        institution_id=institution.id,

        ip_address=get_client_ip(request),

        details={"old_status": old_status.value, "new_status": new_status.value},

        status="SUCCESS"

    )



    return institution
