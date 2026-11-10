from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.models.dataset import Dataset

from app.models.user import User, UserRole

from app.schemas.dataset import DatasetCreate, DatasetResponse

from app.api.deps import get_current_user, require_roles, get_client_ip

from app.services.audit_service import AuditService



router = APIRouter()





@router.get(

    "/",

    response_model=List[DatasetResponse],

    summary="List registered dataset schemas"

)

def list_datasets(

    skip: int = Query(0, ge=0),

    limit: int = Query(50, ge=1, le=100),

    institution_id: Optional[str] = None,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    List registered dataset schemas across institutions.

    NOTE: Only feature schemas, modalities, and sample counts are returned; raw clinical records remain strictly local.

    """

    query = db.query(Dataset)

    if institution_id:

        query = query.filter(Dataset.institution_id == institution_id)

    elif current_user.role == UserRole.HOSPITAL_ADMIN and current_user.institution_id:

        # Hospital Admins default to seeing their own institution's datasets

        query = query.filter(Dataset.institution_id == current_user.institution_id)

    return query.offset(skip).limit(limit).all()





@router.post(

    "/",

    response_model=DatasetResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Register dataset metadata (Hospital Admin only)"

)

def register_dataset(

    dataset_in: DatasetCreate,

    request: Request,

    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.HOSPITAL_ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Register dataset schema metadata for an institution's edge node.

    """

    inst_id = dataset_in.institution_id or current_user.institution_id

    if not inst_id:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Institution ID is required to register dataset metadata."

        )



    # Hospital admins can only register datasets for their own institution

    if current_user.role == UserRole.HOSPITAL_ADMIN and current_user.institution_id != inst_id:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="You are only permitted to register datasets for your own affiliated institution."

        )



    dataset = Dataset(

        institution_id=inst_id,

        name=dataset_in.name.strip(),

        modality=dataset_in.modality,

        sample_count=dataset_in.sample_count,

        feature_schema=dataset_in.feature_schema,

        is_validated=True,

        privacy_budget_spent=0.0

    )



    db.add(dataset)

    db.commit()

    db.refresh(dataset)



    AuditService.log(

        db,

        action="DATASET_SCHEMA_REGISTERED",

        resource_type="DATASET",

        resource_id=dataset.id,

        user_id=current_user.id,

        institution_id=inst_id,

        ip_address=get_client_ip(request),

        details={"name": dataset.name, "sample_count": dataset.sample_count, "modality": dataset.modality.value},

        status="SUCCESS"

    )



    return dataset
