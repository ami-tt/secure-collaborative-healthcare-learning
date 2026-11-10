# Secure Collaborative Healthcare Learning System



[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB.svg)](https://react.dev/)

[![Flower](https://img.shields.io/badge/Federated%20Learning-Flower%20(flwr)-FF6F00.svg)](https://flower.ai/)

[![PyTorch](https://img.shields.io/badge/ML%20Framework-PyTorch-EE4C2C.svg)](https://pytorch.org/)

[![Security](https://img.shields.io/badge/Privacy-Differential%20Privacy%20(DP)-red.svg)](#privacy--security-architecture)



A production-grade, decentralized federated learning platform engineered for hospitals and clinical research centers. The system enables multi-institutional collaborative training of predictive machine learning models without transferring or exposing raw patient datasets.



---



## 🏛 System Architecture Overview



```

                      +---------------------------------------+

                      |         React + Tailwind UI           |

                      | (Admin / Hospital Admin / Researcher) |

                      +-------------------+-------------------+

                                          | HTTPS / WebSockets

                                          v

                      +---------------------------------------+

                      |         FastAPI REST Gateway          |

                      |   (Auth, RBAC, Sessions, Metrics)     |

                      +---------+-------------------+---------+

                                |                   |

                 PostgreSQL DB  |                   | gRPC / Management

                                v                   v

                      +-------------------+   +------------------------------------+

                      | Persistence Layer |   |      Flower FL Server (FedAvg)     |

                      | (Schema, Audits)  |   |  - Weighted Model Aggregation      |

                      +-------------------+   |  - Privacy Budget Accounting       |

                                              +---------+----------------+---------+

                                                        |                |

                                            Secure gRPC |                | Secure gRPC

                                                        v                v

                                              +----------------+  +----------------+

                                              | Hospital A     |  | Hospital B     |

                                              | Local PyTorch  |  | Local PyTorch  |

                                              | + DP-SGD       |  | + DP-SGD       |

                                              | (Local EHR)    |  | (Local EHR)    |

                                              +----------------+  +----------------+

```



---



## 📁 Repository Layout



```

├── backend/            # FastAPI async REST API & WebSocket server

│   ├── app/

│   │   ├── api/v1/     # Modular route handlers (auth, users, fl_sessions, metrics, audit)

│   │   ├── core/       # Configurations, JWT security, DB session management

│   │   ├── models/     # SQLAlchemy relational models

│   │   ├── schemas/    # Pydantic data schemas

│   │   ├── services/   # Business logic & FL orchestration

│   │   └── utils/      # Audit logger & helpers

│   └── requirements.txt

├── federated/          # Flower (flwr) Federated Learning core

│   ├── server/         # FL Server, custom FedAvg strategy, session manager

│   ├── client/         # Hospital edge client runner

│   ├── privacy/        # Differential privacy (noise injection & gradient clipping)

│   └── requirements.txt

├── ml/                 # PyTorch models, synthetic healthcare data, evaluation

│   ├── models/         # Clinical tabular MLP & Medical CNN

│   ├── datasets/       # Synthetic EHR generator & data loaders

│   ├── preprocessing/  # Feature normalizers & categorical encoders

│   ├── evaluation/     # Clinical metrics (ROC-AUC, F1, Sensitivity, Specificity)

│   └── requirements.txt

├── frontend/           # Modern React + Tailwind CSS web interface

│   ├── src/

│   │   ├── components/ # Reusable UI components & Recharts visualizations

│   │   ├── contexts/   # Auth and Session state contexts

│   │   ├── hooks/      # Custom API & WebSocket hooks

│   │   ├── pages/      # Landing page, Auth, Admin, Hospital, Researcher, FL Monitor

│   │   └── services/   # Axios client & WebSocket handlers

│   └── package.json

└── docs/               # Architecture documents and PostgreSQL schema DDL

    ├── architecture/   # Diagrams and system design specs

    └── schema/         # Production SQL schema

```



---



## 👥 Role-Based Access Control (RBAC)



| Role | Responsibilities | Key Capabilities |

| :--- | :--- | :--- |

| **System Admin** | System oversight & compliance | Verify and approve institutions, manage users, inspect HIPAA audit trail, monitor cluster health. |

| **Hospital Administrator** | Institutional data governance | Manage local hospital node, inspect registered dataset schema, allocate privacy budget ($\varepsilon$), monitor local client status. |

| **Researcher** | Clinical model experimentation | Create FL projects, define target conditions, set hyperparameters (rounds, DP epsilon, clipping norm), monitor live convergence. |



---



## 🔒 Privacy & Security Model



1. **Zero Data Movement Principle:** Raw Electronic Health Records (EHR) never exit the hospital boundary.

2. **Differential Privacy (DP-SGD):**

   - Local gradients are clipped to threshold $C$ to bound individual sample sensitivity.

   - Calibrated Gaussian noise $\mathcal{N}(0, \sigma^2)$ is added to guarantee $(\varepsilon, \delta)$-differential privacy.

3. **Stateless Token Authentication:** JSON Web Tokens (JWT) with bcrypt-hashed credentials and fine-grained role authorization.

4. **Immutable Audit Trail:** All administrative, institutional, and training actions are logged with timestamps, user IDs, and client IP addresses.



---



## 🗺️ Next Steps

Review the detailed architecture and database schema in `/docs` and proceed with implementation upon approval.
