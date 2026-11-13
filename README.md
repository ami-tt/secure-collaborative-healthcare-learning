# Secure Collaborative Healthcare Learning System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB.svg)](https://react.dev/)
[![Tailwind](https://img.shields.io/badge/CSS-Tailwind%20CSS-38B2AC.svg)](https://tailwindcss.com/)
[![PyTorch](https://img.shields.io/badge/ML%20Framework-PyTorch-EE4C2C.svg)](https://pytorch.org/)

**Secure Collaborative Healthcare Learning System** is a prototype platform that enables researchers and clinicians to explore cardiovascular disease prediction using real‑world‑like health data. The system provides a modern React UI, a FastAPI backend with JWT‑based authentication, role‑based access control, and a set of machine‑learning models for classification and evaluation.

---

## 📦 Implemented Features

- **FastAPI backend** with asynchronous endpoints.
- **User registration & login** powered by JWT authentication.
- **Role‑Based Access Control (RBAC)** for three roles: System Admin, Hospital Admin, Researcher.
- **SQLAlchemy ORM** models representing users, institutions, datasets, and audit logs.
- **Alembic migrations** for schema versioning.
- **React + Vite frontend** styled with Tailwind CSS.
- **Role‑specific dashboards** (admin, hospital admin, researcher).
- **Cardiovascular disease dataset** preprocessing and exploratory data analysis scripts.
- **Machine‑learning models**:
  - Logistic Regression (scikit‑learn).
  - Multi‑Layer Perceptron (PyTorch).
- **Model evaluation** using Accuracy, Precision, Recall, F1‑score, and ROC‑AUC.
- **Comprehensive test suite** covering backend authentication, RBAC, and basic frontend integration.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React 18, Vite, Tailwind CSS, Recharts (charts), Axios |
| **Backend**   | Python 3.10+, FastAPI, Pydantic, SQLAlchemy, Alembic |
| **Database**  | PostgreSQL (default); SQLite for local quick testing |
| **Machine Learning** | scikit‑learn (Logistic Regression), PyTorch (MLP) |
| **Testing & Development** | pytest, pytest‑asyncio, coverage, pre‑commit, black, isort |

---

## 🏛️ Architecture Overview

```
+-------------------+        HTTPS / WebSocket        +-------------------+
|   React UI (TS)   | <----------------------------> |   FastAPI Server  |
|  (Tailwind CSS)   |                               |  (JWT, RBAC, API) |
+-------------------+                               +---------+---------+
                                                             |
                                                             v
                                                    +-------------------+
                                                    |   PostgreSQL DB   |
                                                    +-------------------+
```

* The frontend communicates with the backend via REST endpoints protected by JWT tokens.
* The backend handles authentication, authorisation, business logic and stores audit logs.
* All persistent data (users, roles, datasets, model artefacts) resides in PostgreSQL.
* Machine‑learning models are trained server‑side using the processed dataset and the results are persisted for later inspection.

---

## 📁 Project Structure

```
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/v1/            # Route handlers (auth, users, datasets, etc.)
│   │   ├── core/               # Configurations, JWT utils, DB session
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   └── services/           # Business‑logic layer
│   └── requirements.txt
│
├── federated/                   # **Planned** Federated Learning components (placeholder)
│   └── README.md               # Contains design notes for future FL integration
│
├── ml/                          # Machine‑learning code and data utilities
│   ├── models/                # PyTorch MLP implementation
│   ├── datasets/               # Synthetic EHR generator & raw CSVs
│   ├── preprocessing/          # Feature scaling, encoding
│   └── evaluation/             # Metric calculations (ROC‑AUC, F1, etc.)
│
├── frontend/                    # React + Vite UI
│   ├── src/
│   │   ├── components/        # Reusable UI components & Recharts visualisations
│   │   ├── contexts/           # Auth and session state
│   │   ├── pages/              # Landing, Login, Register, Dashboards per role
│   │   └── services/           # Axios API wrapper
│   └── package.json
│
├── docs/                        # Architecture diagrams, database schema docs
│   └── ...
│
├── .gitignore
├── README.md
└── alembic.ini                  # Alembic configuration for DB migrations
```

> **Note:** The `federated/` directory contains scaffolding for future federated‑learning work (Flower, differential‑privacy, secure aggregation). It is **not** part of the current functional release.

---

## 📈 Current Development Status

**Completed:** Phase 1 – 3 (core backend, frontend UI, dataset processing, ML models, tests).

**Planned next steps:**
- Flower‑based Federated Learning (FedAvg) integration.
- Differential Privacy mechanisms.
- Secure aggregation of model updates.
- Live training monitoring dashboard.
- Production‑grade deployment, scalability and security hardening.

---

## 📊 Dataset & Disclaimer

The project ships a **cardiovascular disease dataset** (derived from public UCI data) that mimics real electronic health records. It is used for demonstrating preprocessing, feature engineering, and model training. **This prototype is for educational and research purposes only and is not a clinically validated diagnostic tool.** Users should not rely on the predictions for real patient care.

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone <repo-url>
cd "New folder (2)"
```

### Backend

```bash
# Create a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and set DATABASE_URL (e.g. postgresql://user:pass@localhost:5432/healthcare_fl_db)

# Run database migrations
alembic -c alembic.ini upgrade head

# Start the FastAPI server
uvicorn backend/app/main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
# Development server
npm run dev
# To build for production
npm run build
```

The UI will be served at `http://localhost:5173` (default Vite port).

### Running Tests

```bash
# Backend tests
pytest backend/tests -v

# ML pipeline tests
pytest ml/tests -v
```

All tests should pass on a fresh clone.

---

## License

No open-source license has been specified yet. All rights are reserved by the project author unless otherwise stated.

---

*For any questions or contributions, please open an issue or submit a pull request.*

---

## 📦 Deploying Secure Collaborative Healthcare Learning System

### Overview
The **Secure Collaborative Healthcare Learning System** is a prototype platform that supports the first three phases of the project (core backend, frontend UI, and machine‑learning models). Future phases such as Federated Learning, Differential Privacy, Secure Aggregation, and live monitoring are only scaffolding at the moment and are **not** part of the production release.

---

## 🛠️ Implemented Features (Phase 1‑3)

- FastAPI backend with JWT‑based authentication and role‑based access control (System Admin, Hospital Admin, Researcher).
- Asynchronous CRUD endpoints for users, institutions, datasets, and audit logs.
- SQLite support for local development and PostgreSQL for production.
- Alembic migrations for schema versioning.
- React 18 frontend (Vite) styled with Tailwind CSS.
- Machine‑learning pipelines (Logistic Regression, PyTorch MLP) for cardiovascular disease prediction.
- Comprehensive test suite covering authentication, RBAC, and core business logic.

---

## 🏗️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | React 18, Vite, Tailwind CSS, Recharts, Axios |
| **Backend** | Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic |
| **Database** | PostgreSQL (production) – SQLite (local dev) |
| **ML** | scikit‑learn (Logistic Regression), PyTorch (MLP) |
| **Testing** | pytest, pytest‑asyncio, coverage |

---

## 📁 Project Structure

```text
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/v1/            # Route handlers (auth, users, etc.)
│   │   ├── core/               # Settings, DB engine, JWT utils
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   └── services/           # Business‑logic layer
│   └── requirements.txt
│
├── federated/                   # Placeholder for future federated‑learning work
│   └── README.md               # Design notes (future phases only)
│
├── ml/                          # Machine‑learning code and data utilities
│   ├── models/                # PyTorch MLP implementation
│   ├── datasets/               # Synthetic EHR generator & raw CSVs
│   └── evaluation/             # Metrics (ROC‑AUC, F1, etc.)
│
├── frontend/                    # React + Vite UI
│   └── src/ …
│
├── alembic/                     # Database migration scripts
│   └── versions/ …
│
├── .gitignore
├── Procfile                     # Render process definition (added)
├── README.md                    # This document
└── alembic.ini                  # Alembic configuration
```

---

## ⚙️ Local Installation

### Backend

```bash
# Clone the repository (already done)
# Create a virtual environment
python -m venv .venv
# Activate (PowerShell)
.venv\Scripts\Activate.ps1
# Install dependencies
pip install -r backend/requirements.txt

# Copy example env and adjust for local dev
cp backend/.env.example backend/.env
# Edit backend/.env – set DATABASE_URL to SQLite (default) or a local PostgreSQL instance
# Example for SQLite (default):
# DATABASE_URL=sqlite:///./healthcare_fl.db
# Example for local PostgreSQL:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/healthcare_fl_dev

# Run migrations (creates tables for the chosen DB)
alembic -c alembic.ini upgrade head

# Start the FastAPI server (development mode)
uvicorn backend/app/main:app --reload
```

The API will be reachable at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
# Development server
npm run dev   # Vite serves on http://localhost:5173
# Production build
npm run build
```

---

## 🗄️ Database Requirements

- **Production**: PostgreSQL 12+ (recommended on Render). A single database URL is required, e.g.
  `postgresql://USER:PASSWORD@HOST:5432/DATABASE_NAME`.
- **Local Development**: SQLite works out of the box; alternatively you can point `DATABASE_URL` to a local PostgreSQL instance.
- Alembic migrations are stored in `backend/alembic/`. Running `alembic -c alembic.ini upgrade head` applies the latest schema.

---

## 🚀 Render Backend Deployment

1. **Add a Procfile** (already present at the repo root):
   ```
   web: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
   Render automatically supplies the `$PORT` environment variable; the command binds to `0.0.0.0` as required.
2. **Create a Render Web Service** and point it at the repository.
3. **Set the following environment variables** in the Render dashboard (values are placeholders – replace with your secrets):
   - `ENVIRONMENT=production`
   - `SECRET_KEY=<32‑character‑random‑secret>`
   - `DATABASE_URL=postgresql://user:password@host:5432/dbname`
   - `PROVISION_SUPERADMIN=true` *(optional, only if you want the initial admin created)*
   - `FIRST_SUPERADMIN_EMAIL=admin@securefl.health` *(required when provisioning)*
   - `FIRST_SUPERADMIN_PASSWORD=<≥12‑character‑password>` *(required when provisioning)*
   - `BACKEND_CORS_ORIGINS=https://<your‑frontend>.vercel.app` *(no wildcards)*
4. **Build Command** (Render): `pip install -r backend/requirements.txt`
5. **Start Command**: Render will use the Procfile automatically.
6. **Migrations**: Render runs the start command after the build step. The first request will trigger the FastAPI app which, on startup, will call Alembic’s `upgrade head` if you add it to a **post‑install script** or run it manually via a Render **Shell** command:
   ```bash
   alembic -c alembic.ini upgrade head
   ```
7. **Security notes** – `settings` disables loading a local `.env` file in production (`env_file=None`), so all secrets must be supplied via Render’s UI. Debug mode is forced off, SQLite URLs are rejected, and wildcard CORS origins are not allowed.

---

## 🌐 Vercel Frontend Deployment

1. Push the `frontend/` folder to a Vercel project (connect the repository and select the `frontend/` directory as the root).
2. Vercel automatically runs `npm install` and `npm run build`.
3. Set the **Environment Variable** `NEXT_PUBLIC_API_URL` (or similar) to the Render backend URL, e.g. `https://my‑backend.onrender.com`.
4. Ensure the backend’s `BACKEND_CORS_ORIGINS` includes the Vercel domain (`https://<your‑frontend>.vercel.app`).

---

## 🌐 CORS Configuration

The backend reads `BACKEND_CORS_ORIGINS` (list or comma‑separated string). In production you must provide an explicit list of allowed origins – a wildcard (`*`) will cause a validation error. Example:
```
BACKEND_CORS_ORIGINS=https://myapp.vercel.app,https://admin.myapp.vercel.app
```

---

## 🧪 Testing

```bash
# Backend tests
pytest backend/tests -v
# Frontend (if any) – run via npm scripts defined in package.json
```
All tests pass (`30 passed, 0 failed`).

---

## 🔐 Security Considerations

- **Never commit** real secrets. `.env` files are ignored via `.gitignore`.
- Production requires a **strong `SECRET_KEY`** (≥ 32 characters) – the config validator rejects placeholders.
- `DEBUG` is forced off in production.
- SQLite is disallowed for production deployments.
- Admin provisioning is explicit; no default production passwords exist.
- CORS origins must be whitelisted; wildcards are rejected.

---

## 📖 Future Development (Phase 4+)

- **Federated Learning** (Flower integration)
- **Differential Privacy** mechanisms
- **Secure Aggregation** of model updates
- **Live monitoring dashboards**

These components are currently only scaffolding under the `federated/` directory and are **not** part of the deployed backend.

---

*For any questions or contributions, please open an issue or submit a pull request.*
