# System Architecture: Secure Collaborative Healthcare Learning System



## 1. Executive Summary

The **Secure Collaborative Healthcare Learning System** is a decentralized, privacy-preserving machine learning platform engineered for clinical institutions (hospitals, diagnostic centers, research institutes). It enables cross-institutional model training without sharing confidential Electronic Health Records (EHR) or patient identifiable information (PII).



The platform addresses three core challenges in modern healthcare AI:

1. **Data Silos & Scarcity:** Individual hospitals lack sufficient data diversity for rare or heterogeneous diseases.

2. **Regulatory & Privacy Mandates:** HIPAA, GDPR, and local privacy laws penalize centralization of sensitive medical records.

3. **Model Inversion & Reconstruction Attacks:** Even without sharing raw data, naive sharing of model gradients can leak patient records. The platform counters this via **Differential Privacy (DP-SGD)** and **Secure Parameter Aggregation (FedAvg)**.



---



## 2. Architecture Overview



```mermaid

flowchart TB

    subgraph UI_Layer ["Presentation Tier (React 18 + Tailwind CSS)"]

        Landing["Public Landing Page"]

        AdminDash["Admin Control Panel"]

        HospitalDash["Hospital Admin Portal"]

        ResearchDash["Researcher Studio"]

        FLMonitor["Real-time Convergence Monitor (Recharts)"]

    end



    subgraph API_Layer ["API & Orchestration Tier (FastAPI Async)"]

        Gateway["REST API Gateway & RBAC Middleware"]

        AuthSvc["JWT Auth & Institution Identity"]

        SessionMgr["FL Session Orchestrator"]

        MetricStream["WebSocket Real-Time Streamer"]

        AuditSvc["HIPAA Audit Logger"]

    end



    subgraph DB_Layer ["Persistence Tier (PostgreSQL)"]

        Postgres[(PostgreSQL Relational DB)]

        Storage[(Model Checkpoint Vault / Checksums)]

    end



    subgraph FL_Layer ["Federated Learning Tier (Flower Server)"]

        FlowerServer["Flower FL Aggregator (flwr)"]

        FedAvgEngine["Secure FedAvg Strategy"]

        DPEvaluator["Differential Privacy Budget Tracker"]

    end



    subgraph Hospital_A ["Hospital Node A (Edge Client)"]

        LocalDataA[("Local EHR Data (Never Leaves)")]

        LocalTrainerA["PyTorch Local Model + DP-SGD"]

        ClientA["Flower Client A"]

    end



    subgraph Hospital_B ["Hospital Node B (Edge Client)"]

        LocalDataB[("Local EHR Data (Never Leaves)")]

        LocalTrainerB["PyTorch Local Model + DP-SGD"]

        ClientB["Flower Client B"]

    end



    %% Connections

    UI_Layer -->|HTTPS / REST & WSS| API_Layer

    API_Layer -->|SQLAlchemy ORM| DB_Layer

    SessionMgr -->|gRPC / RPC Trigger| FlowerServer

    FlowerServer -->|Secure gRPC| ClientA

    FlowerServer -->|Secure gRPC| ClientB

    ClientA --> LocalTrainerA --> LocalDataA

    ClientB --> LocalTrainerB --> LocalDataB

    FlowerServer -->|Metrics & Checkpoints| DB_Layer

    MetricStream -.->|Push Round Metrics| FLMonitor

```



---



## 3. Core Subsystems



### 3.1. Frontend Tier (`frontend/`)

- **Technology:** React.js, Tailwind CSS, Recharts, Lucide Icons, Vite.

- **Role-Based Views:**

  - **Super Admin:** Institution approvals, system telemetry, global audit trails, user RBAC management.

  - **Hospital Administrator:** Local node configuration, local dataset schema validation, privacy budget allowance, client heartbeat.

  - **Researcher:** Experiment creator, hyperparameter tuning ($\varepsilon, \delta$, clipping norm, rounds), real-time loss/accuracy monitoring, model checkpoint download.

- **Telemetry:** WebSocket connection for real-time loss curves, ROC-AUC, round times, and client participation indicators.



### 3.2. Backend & API Tier (`backend/`)

- **Technology:** FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Python-JOSE (JWT), Passlib/Bcrypt.

- **Security & Authorization:**

  - Token-based stateless authentication (JWT with expiration and refresh mechanism).

  - Fine-grained RBAC decorators (`@require_roles(["admin"])`).

  - Request verification, rate-limiting, and input sanitization.

- **WebSocket Streaming:**

  - Pushes live round-by-round training metrics to active research sessions.



### 3.3. Federated Learning Core (`federated/`)

- **Technology:** Flower Framework (`flwr`), gRPC.

- **Strategy:** Federated Averaging (`FedAvg`) extended with:

  - Minimum client threshold enforcement.

  - Validation metrics aggregation (weighted by client dataset sizes).

  - Fault tolerance (straggler mitigation and dropped client recovery).



### 3.4. Machine Learning & Privacy Layer (`ml/` & `federated/privacy/`)

- **Technology:** PyTorch, Scikit-learn, NumPy.

- **Differential Privacy (DP):**

  - **Gradient Clipping:** Clips the $L_2$ norm of gradients at threshold $C$:

    $$g \leftarrow g / \max\left(1, \frac{\|g\|_2}{C}\right)$$

  - **Calibrated Noise Injection:** Gaussian noise calibrated against privacy parameters $(\varepsilon, \delta)$:

    $$\sigma = \frac{\sqrt{2\ln(1.25/\delta)} \cdot C}{\varepsilon}$$

  - **Privacy Budget Accounting:** Tracks cumulative $(\varepsilon, \delta)$ spent across rounds to guarantee strict privacy guarantees.

- **Clinical Task Models:**

  - Tabular MLP for EHR risk stratification (e.g., Diabetes/Cardiovascular/Sepsis classification).

  - Convolutional Neural Network (CNN) architecture designed for medical imaging (e.g., Chest X-Ray pneumonia classification).



---



## 4. Sequence: A Single Federated Training Round



```mermaid

sequenceDiagram

    autonumber

    actor Researcher

    participant Web as Dashboard UI

    participant Backend as FastAPI Orchestrator

    participant FLServer as Flower FL Server

    participant NodeA as Hospital Node A

    participant NodeB as Hospital Node B

    participant DB as PostgreSQL



    Researcher->>Web: Launch FL Session (Target: EHR, Rounds: 10, DP-Epsilon: 1.5)

    Web->>Backend: POST /api/v1/fl/sessions/start

    Backend->>DB: Update Session Status -> "IN_PROGRESS"

    Backend->>FLServer: Initialize Server with Global Initial Weights $W_0$



    loop Every Round t = 1 to T

        FLServer->>NodeA: Send Global Parameters $W_{t-1}$

        FLServer->>NodeB: Send Global Parameters $W_{t-1}$



        par Local DP Training (Hospital A)

            NodeA->>NodeA: Train PyTorch model on local EHR data

            NodeA->>NodeA: Clip Gradients ($L_2 \le C$) & Add Gaussian Noise $\mathcal{N}(0, \sigma^2)$

            NodeA->>FLServer: Send Local Updated Weights $W_t^A$ & Sample Count $n_A$

        and Local DP Training (Hospital B)

            NodeB->>NodeB: Train PyTorch model on local EHR data

            NodeB->>NodeB: Clip Gradients ($L_2 \le C$) & Add Gaussian Noise $\mathcal{N}(0, \sigma^2)$

            NodeB->>FLServer: Send Local Updated Weights $W_t^B$ & Sample Count $n_B$

        end



        FLServer->>FLServer: Aggregate: $W_t = \sum \frac{n_k}{N} W_t^k$ (FedAvg)

        FLServer->>FLServer: Compute Validation Loss, Accuracy, ROC-AUC

        FLServer->>Backend: Push Round $t$ Metrics & Checkpoint

        Backend->>DB: Store Metrics & Checkpoint File Path

        Backend-->>Web: WebSocket Broadcast (Round $t$ Loss & Convergence)

    end



    Backend->>DB: Update Session Status -> "COMPLETED"

    Backend-->>Web: Notify Session Complete & Provide Download Token

```
