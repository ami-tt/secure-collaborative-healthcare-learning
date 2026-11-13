import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse, FileResponse

from fastapi.staticfiles import StaticFiles

from fastapi.openapi.utils import get_openapi

from sqlalchemy import text



from app.core.config import settings

from app.core.database import SessionLocal

from app.db.init_db import init_db

from app.api.v1.router import api_router





@asynccontextmanager

async def lifespan(app: FastAPI):

    """

    Application lifecycle manager:

    Executes database table creation and seed data insertion upon startup.

    """

    db = SessionLocal()

    try:
        # Seed data only in development environment
        if settings.ENVIRONMENT != "production":
            init_db(db)
    finally:
        db.close()

    yield





app = FastAPI(

    title=settings.PROJECT_NAME,

    version=settings.VERSION,

    description="""

## Secure Collaborative Healthcare Learning System (Backend API)



A decentralized, privacy-preserving machine learning platform for clinical institutions.

Enables cross-institutional collaborative training of machine learning models without sharing patient-level Electronic Health Records (EHR).



### Key Features

- **Stateless JWT Authentication:** Secure bearer tokens with role-based claims.

- **Role-Based Access Control (RBAC):** Three distinct roles:

  - `admin`: Platform governance, institution approval, HIPAA audit trail.

  - `hospital_admin`: Local edge node configuration, dataset schema verification, privacy budget control.

  - `researcher`: Federated study creation, model hyperparameter tuning, convergence monitoring.

- **Data Sovereignty:** Zero raw patient records leave hospital firewalls.

- **Differential Privacy & FedAvg Ready:** Pre-architected data structures for gradient clipping, noise injection, and weighted parameter aggregation.

- **HIPAA / GDPR Compliance:** Immutable audit logging for all sensitive platform events.

    """,

    lifespan=lifespan,

    docs_url="/docs",

    redoc_url="/redoc"

)



# Configure Cross-Origin Resource Sharing (CORS)

app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.BACKEND_CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# Mount API v1 Routers

app.include_router(api_router, prefix=settings.API_V1_STR)



# Locate and mount static frontend directory

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if os.path.exists(STATIC_DIR):

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")





@app.get(

    "/",

    tags=["General"],

    summary="Interactive Web Application & Service Status"

)

def root(request: Request):

    """

    Serves the interactive healthcare SaaS frontend if accessed via browser,

    or returns API discovery JSON if requested by programmatic API clients.

    """

    accept = request.headers.get("accept", "")

    index_file = os.path.join(STATIC_DIR, "index.html")

    if "text/html" in accept and os.path.exists(index_file):

        return FileResponse(index_file)



    return {

        "project": settings.PROJECT_NAME,

        "version": settings.VERSION,

        "environment": settings.ENVIRONMENT,

        "status": "online",

        "web_application": "/app",

        "documentation": {

            "swagger_ui": "/docs",

            "redoc": "/redoc"

        },

        "api_v1": settings.API_V1_STR

    }





@app.get(

    "/app",

    tags=["General"],

    summary="Interactive Frontend Dashboard"

)

def web_app():

    """Serves the interactive healthcare SaaS single page application."""

    index_file = os.path.join(STATIC_DIR, "index.html")

    if os.path.exists(index_file):

        return FileResponse(index_file)

    return JSONResponse(status_code=404, content={"message": "Frontend bundle not found"})





@app.get(

    "/health",

    tags=["General"],

    summary="Health check & database probe"

)

def health_check():

    """Validates API process health and database connectivity."""

    db_status = "healthy"

    try:

        db = SessionLocal()

        db.execute(text("SELECT 1"))

        db.close()

    except Exception as e:

        db_status = f"unhealthy: {str(e)}"



    return {

        "status": "healthy" if db_status == "healthy" else "degraded",

        "database": db_status,

        "version": settings.VERSION,

        "environment": settings.ENVIRONMENT

    }





def custom_openapi():

    """Customizes OpenAPI schema to declare Bearer token authentication globally."""

    if app.openapi_schema:

        return app.openapi_schema



    openapi_schema = get_openapi(

        title=settings.PROJECT_NAME,

        version=settings.VERSION,

        description=app.description,

        routes=app.routes,

    )

    openapi_schema["components"]["securitySchemes"] = {

        "BearerAuth": {

            "type": "http",

            "scheme": "bearer",

            "bearerFormat": "JWT",

            "description": "Enter your JWT token in the format: Bearer <token>"

        }

    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema





app.openapi = custom_openapi
