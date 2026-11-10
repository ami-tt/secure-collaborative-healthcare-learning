from fastapi import APIRouter

from app.api.v1 import auth, users, institutions, datasets, fl_sessions, audit



api_router = APIRouter()



api_router.include_router(

    auth.router,

    prefix="/auth",

    tags=["Authentication & Authorization"]

)

api_router.include_router(

    users.router,

    prefix="/users",

    tags=["User Management & RBAC"]

)

api_router.include_router(

    institutions.router,

    prefix="/institutions",

    tags=["Healthcare Institutions"]

)

api_router.include_router(

    datasets.router,

    prefix="/datasets",

    tags=["Dataset Metadata & Schemas"]

)

api_router.include_router(

    fl_sessions.router,

    prefix="/fl",

    tags=["Federated Learning Orchestration"]

)

api_router.include_router(

    audit.router,

    prefix="/audit",

    tags=["Security & Compliance Audit Trail"]

)
