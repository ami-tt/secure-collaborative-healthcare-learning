from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.models.fl_project import FLProject

from app.models.fl_session import FLSession, SessionStatus

from app.models.user import User, UserRole

from app.schemas.fl_session import (

    FLProjectCreate, FLProjectResponse,

    FLSessionCreate, FLSessionResponse

)

from app.api.deps import get_current_user, require_roles, get_client_ip

from app.services.audit_service import AuditService



router = APIRouter()





@router.get(

    "/projects",

    response_model=List[FLProjectResponse],

    summary="List collaborative research projects"

)

def list_projects(

    skip: int = Query(0, ge=0),

    limit: int = Query(50, ge=1, le=100),

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    List all registered collaborative research projects.

    """

    return db.query(FLProject).offset(skip).limit(limit).all()





@router.post(

    "/projects",

    response_model=FLProjectResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Create a new research project (Researcher or Admin)"

)

def create_project(

    project_in: FLProjectCreate,

    request: Request,

    current_user: User = Depends(require_roles([UserRole.RESEARCHER, UserRole.ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Create a new clinical FL project specifying target disease condition and model architecture.

    """

    project = FLProject(

        title=project_in.title.strip(),

        description=project_in.description,

        target_condition=project_in.target_condition.strip(),

        model_architecture=project_in.model_architecture,

        modality=project_in.modality,

        created_by=current_user.id

    )



    db.add(project)

    db.commit()

    db.refresh(project)



    AuditService.log(

        db,

        action="FL_PROJECT_CREATED",

        resource_type="FL_PROJECT",

        resource_id=project.id,

        user_id=current_user.id,

        ip_address=get_client_ip(request),

        details={"title": project.title, "condition": project.target_condition},

        status="SUCCESS"

    )



    return project





@router.get(

    "/sessions",

    response_model=List[FLSessionResponse],

    summary="List training sessions"

)

def list_sessions(

    project_id: Optional[str] = None,

    status_filter: Optional[SessionStatus] = None,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    """

    List federated training sessions optionally filtered by project or execution status.

    """

    query = db.query(FLSession)

    if project_id:

        query = query.filter(FLSession.project_id == project_id)

    if status_filter:

        query = query.filter(FLSession.status == status_filter)

    return query.all()





@router.post(

    "/sessions",

    response_model=FLSessionResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Create a federated training run configuration (Researcher or Admin)"

)

def create_session(

    session_in: FLSessionCreate,

    request: Request,

    current_user: User = Depends(require_roles([UserRole.RESEARCHER, UserRole.ADMIN])),

    db: Session = Depends(get_db)

):

    """

    Configure a new federated learning training run with privacy budget and aggregation settings.

    """

    project = db.query(FLProject).filter(FLProject.id == session_in.project_id).first()

    if not project:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"Parent project '{session_in.project_id}' was not found."

        )



    session = FLSession(

        project_id=session_in.project_id,

        session_name=session_in.session_name.strip(),

        total_rounds=session_in.total_rounds,

        min_participating_clients=session_in.min_participating_clients,

        aggregation_strategy=session_in.aggregation_strategy,

        dp_enabled=session_in.dp_enabled,

        dp_epsilon=session_in.dp_epsilon,

        dp_delta=session_in.dp_delta,

        dp_max_grad_norm=session_in.dp_max_grad_norm,

        learning_rate=session_in.learning_rate,

        local_epochs=session_in.local_epochs,

        batch_size=session_in.batch_size,

        status=SessionStatus.CREATED

    )



    db.add(session)

    db.commit()

    db.refresh(session)



    AuditService.log(

        db,

        action="FL_SESSION_CONFIGURED",

        resource_type="FL_SESSION",

        resource_id=session.id,

        user_id=current_user.id,

        ip_address=get_client_ip(request),

        details={"name": session.session_name, "rounds": session.total_rounds, "dp_epsilon": session.dp_epsilon},

        status="SUCCESS"

    )



    return session
