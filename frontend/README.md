# Frontend Module: Secure Collaborative Healthcare Learning System



The frontend interface for the **Secure Collaborative Healthcare Learning System** is engineered as a modern, high-performance healthcare AI SaaS platform using **React 18**, **Tailwind CSS**, and **Recharts**.



---



## 🎨 Design System & Visual Identity

- **Backgrounds**: Crisp whites (`#ffffff`), soft medical light grays (`#f8fafc`, `bg-slate-50`).

- **Accents**: Deep clinical navy blue (`text-slate-900`, `bg-slate-900`) and vibrant surgical teal (`#0d9488`, `text-teal-600`, `bg-teal-600`).

- **Typography**: Clean, accessible sans-serif (`Inter`) with strict visual hierarchy.

- **Micro-interactions**: Subtle hover elevations, animated pulse badges for live edge nodes, and smooth modal transitions.



---



## 📱 Implemented Pages & Features



### 1. Landing Page (`src/pages/landing/LandingPage.jsx`)

- Professional hero banner with decentralized clinical AI value proposition.

- 4-step architectural breakdown of Federated Averaging (FedAvg) and Differential Privacy (DP-SGD).

- Regulatory compliance highlights (HIPAA, GDPR, Zero Data Movement guarantee).

- Live telemetry preview card and call-to-action buttons.



### 2. Authentication Portal (`src/pages/auth/`)

- **Login (`LoginPage.jsx`)**: Email & password authentication with JWT storage in `localStorage`. Includes **Instant Demo Credentials** buttons for testing as Admin, Hospital Admin, or Researcher with one click.

- **Registration (`RegisterPage.jsx`)**: Multi-role registration (Researcher, Hospital Administrator, System Admin) with institutional affiliation and email validation.



### 3. System Admin Dashboard (`src/pages/admin/AdminDashboard.jsx`)

- Network summary stat cards (Hospitals, Users, FL Runs, Audit Logs).

- Hospital Management: Onboard new clinical partners, inspect metadata, approve or suspend institutions.

- Platform User Directory: Inspect accounts, roles, and verification states.

- System-wide immutable HIPAA audit trail viewer.



### 4. Hospital Administrator Dashboard (`src/pages/hospital/HospitalDashboard.jsx`)

- Edge Client Node status and institutional credentials.

- Local Dataset Management: Register local patient cohorts (metadata and feature schemas only — **zero raw patient records leave premises**).

- Edge training status and local Differential Privacy budget ($\varepsilon$) tracker.



### 5. Clinical Researcher Studio (`src/pages/researcher/ResearcherDashboard.jsx`)

- Research Studies Management: Create clinical initiatives specifying target conditions (e.g., Cardiovascular Risk, Sepsis) and neural architectures (`TabularMLP` vs `ClinicalCNN`).

- Federated Training Runs: Configure hyperparameters (total rounds, minimum hospital threshold, batch size, learning rate, and Differential Privacy parameters $\varepsilon, C$).

- Direct link to the live telemetry monitoring room.



### 6. Federated Learning Monitoring (`src/pages/fl_monitor/FLMonitorDashboard.jsx`)

- Real-time training round stepper and progress bar.

- Recharts-powered **Convergence LineChart** displaying Global Accuracy and Loss curves.

- Recharts-powered **Client Performance Distribution** comparing hospital sample sizes and local accuracies.

- Connected hospital node partition matrix with live edge node heartbeats.

- Global PyTorch model weight artifact vault with SHA-256 integrity checksum verification.



### 7. Security & Compliance Dashboard (`src/pages/security/SecurityDashboard.jsx`)

- Full regulatory audit ledger with search and outcome filtering (`SUCCESS`, `FAILED`, `UNAUTHORIZED`).

- Real-time IP address tracking and client action audit.

- Differential Privacy loss parameters ($\varepsilon \le 1.5$) enforcement check.



---



## 🚀 Running the Frontend



### Method 1: Instant Zero-Install Access (Recommended)

The frontend is already built and mounted directly into the FastAPI backend service.



Simply start the backend:

```bash

cd backend

python run.py

```

Then open your web browser to:

👉 **[http://localhost:8000/app](http://localhost:8000/app)** (or [http://localhost:8000/](http://localhost:8000/))



You can immediately:

1. View the landing page.

2. Click **Sign In** and click any of the instant demo buttons (`Super Admin`, `Hospital Admin`, `Researcher`).

3. Manage hospitals, register dataset schemas, configure FL studies, and watch the live telemetry curves.



### Method 2: Standalone Vite Dev Server (When Node.js is installed)

```bash

cd frontend

npm install

npm run dev

```

The Vite development server will start at `http://localhost:5173`, automatically proxying `/api` requests to the FastAPI backend at `http://localhost:8000`.



---



## 🧪 Testing Results

All frontend and backend integration tests pass with 100% success rate:

```bash

python -m pytest backend/tests/ -v

# 20 passed in 4.67s

```
