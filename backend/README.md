# Backend Module: FastAPI Orchestrator & REST APIs



The backend service for the **Secure Collaborative Healthcare Learning System** provides asynchronous REST APIs, stateless JWT-based Role-Based Access Control (RBAC), database persistence via SQLAlchemy 2.0 with Alembic migrations, and an immutable HIPAA/GDPR audit trail.



---



## 🛠 Features Implemented in Phase 1



1. **FastAPI Web Service:**

   - Asynchronous request handling with lifespan hooks for automatic table generation and data seeding.

   - Comprehensive Swagger UI (`/docs`) and ReDoc (`/redoc`) with global Bearer JWT security scheme.

   - Global health monitoring endpoint (`/health`) with live database probe.



2. **Database Architecture & SQLAlchemy Models:**

   - 10 Relational Models with UUID primary keys and UTC timestamp tracking:

     - `User`: Roles (`admin`, `hospital_admin`, `researcher`), password hashes, verification flags, last login.

     - `Institution`: Healthcare institution metadata, verification statuses, and client API keys.

     - `Dataset`: Registered dataset schemas (feature lists, sample counts, modality) — **zero raw data movement**.

     - `FLProject` & `FLSession`: Clinical research initiatives and training run parameters.

     - `FLSessionParticipant`: Edge client connectivity and last heartbeat.

     - `FLRoundMetric` & `FLClientRoundMetric`: Global and local round performance telemetry.

     - `ModelCheckpoint`: Serialized PyTorch weight metadata, metrics summaries, and SHA-256 integrity checksums.

     - `AuditLog`: Immutable compliance records with user IDs, IP addresses, resource types, and execution timestamps.



3. **Authentication & Security:**

   - **Password Hashing:** Native `bcrypt` with randomized salt (12 rounds) and length truncation guard.

   - **JWT Tokens:** Signed with HMAC-SHA256 (`HS256`), containing role claims, institution IDs, and expiration timestamps.

   - **Role-Based Access Control (RBAC):** Strict dependency guards (`require_roles([UserRole.ADMIN, ...])`) denying unauthorized roles with `HTTP 403 Forbidden`.



4. **Alembic Database Migrations:**

   - Fully configured environment (`alembic.ini` and `alembic/env.py`) dynamically reading runtime database settings.

   - Initial schema revision generated and applied (`29c49cb47e68_initial_schema.py`).



5. **Automated Testing Suite:**

   - 10 comprehensive tests covering authentication, token validation, RBAC rejection, hospital registration, dataset registration, project creation, and audit logging.



---



## 🚀 Running the Backend Locally



### 1. Prerequisites

- Python 3.10+ (tested on Python 3.14)

- PostgreSQL 14+ (optional, SQLite is enabled by default for zero-setup development)



### 2. Install Dependencies

```bash

cd backend

pip install -r requirements.txt

```



### 3. Environment Configuration

Duplicate `.env.example` to `.env` (already created with sensible development defaults):

```bash

cp .env.example .env

```



To connect to a production **PostgreSQL** database, update `DATABASE_URL` in `.env`:

```ini

DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/healthcare_fl_db"

```



### 4. Initialize Database & Seed Baseline Records

Run the initialization script to create tables and seed default users:

```bash

python -m app.db.init_db

```



Default seeded credentials:

| Role | Email | Password | Affiliation |

| :--- | :--- | :--- | :--- |

| **System Admin** | `admin@securefl.health` | `AdminSecurePassword123!` | System-wide |

| **Hospital Administrator** | `hospadmin@hospital-alpha.org` | `HospAdmin123!` | Alpha Health Cardiology Center |

| **Clinical Researcher** | `researcher@fl-research.org` | `Researcher123!` | Global Research Cohort |



### 5. Start the Server

```bash

python run.py

```

Or with uvicorn directly:

```bash

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```



The interactive API documentation is available at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)



---



## 🧪 Running Automated Tests

```bash

python -m pytest tests/test_auth_rbac.py -v

```

All 10 test cases validate complete end-to-end functionality.



---



## 📂 Directory Layout

```

backend/

├── alembic/                # Alembic database migrations

│   ├── versions/           # Migration revisions

│   └── env.py              # Dynamic migration environment

├── app/

│   ├── api/                # API router definitions

│   │   ├── deps.py         # Auth, JWT & RBAC dependencies

│   │   └── v1/             # Modular v1 endpoints

│   │       ├── auth.py

│   │       ├── users.py

│   │       ├── institutions.py

│   │       ├── datasets.py

│   │       ├── fl_sessions.py

│   │       └── audit.py

│   ├── core/               # Configuration, security & database engine

│   ├── db/                 # Database initialization & seeding scripts

│   ├── models/             # SQLAlchemy 2.0 ORM models

│   ├── schemas/            # Pydantic v2 schemas

│   ├── services/           # Business logic & audit logging

│   └── main.py             # FastAPI entrypoint

├── tests/                  # Pytest test suite

├── .env                    # Runtime environment variables

├── .env.example            # Environment template

├── alembic.ini             # Alembic configuration

├── requirements.txt        # Backend dependencies

└── run.py                  # Local startup script

```
