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