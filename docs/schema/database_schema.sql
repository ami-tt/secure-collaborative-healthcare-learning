-- ==============================================================================

-- Secure Collaborative Healthcare Learning System

-- Production Database Schema (PostgreSQL 14+)

-- ==============================================================================



-- Drop tables if already existing for clean rebuild (in reverse dependency order)

DROP TABLE IF EXISTS audit_logs CASCADE;

DROP TABLE IF EXISTS model_checkpoints CASCADE;

DROP TABLE IF EXISTS fl_client_round_metrics CASCADE;

DROP TABLE IF EXISTS fl_round_metrics CASCADE;

DROP TABLE IF EXISTS fl_session_participants CASCADE;

DROP TABLE IF EXISTS fl_sessions CASCADE;

DROP TABLE IF EXISTS fl_projects CASCADE;

DROP TABLE IF EXISTS datasets CASCADE;

DROP TABLE IF EXISTS users CASCADE;

DROP TABLE IF EXISTS institutions CASCADE;



-- Drop Enums if existing

DROP TYPE IF EXISTS user_role_enum CASCADE;

DROP TYPE IF EXISTS institution_status_enum CASCADE;

DROP TYPE IF EXISTS session_status_enum CASCADE;

DROP TYPE IF EXISTS client_status_enum CASCADE;

DROP TYPE IF EXISTS model_modality_enum CASCADE;



-- ------------------------------------------------------------------------------

-- ENUM TYPES

-- ------------------------------------------------------------------------------

CREATE TYPE user_role_enum AS ENUM (

    'admin',

    'hospital_admin',

    'researcher'

);



CREATE TYPE institution_status_enum AS ENUM (

    'pending_verification',

    'active',

    'suspended',

    'decommissioned'

);



CREATE TYPE session_status_enum AS ENUM (

    'created',

    'waiting_for_clients',

    'in_progress',

    'converged',

    'completed',

    'failed',

    'cancelled'

);



CREATE TYPE client_status_enum AS ENUM (

    'registered',

    'connected',

    'training',

    'submitting',

    'idle',

    'disconnected',

    'error'

);



CREATE TYPE model_modality_enum AS ENUM (

    'tabular_ehr',

    'medical_imaging',

    'clinical_notes_nlp'

);



-- ------------------------------------------------------------------------------

-- TABLE: institutions

-- Description: Healthcare institutions (Hospitals, Diagnostic Centers) participating in FL

-- ------------------------------------------------------------------------------

CREATE TABLE institutions (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,

    institution_code VARCHAR(50) UNIQUE NOT NULL,

    contact_email VARCHAR(255) NOT NULL,

    phone VARCHAR(50),

    address TEXT,

    api_key_hash VARCHAR(255) NOT NULL,

    status institution_status_enum NOT NULL DEFAULT 'pending_verification',

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: users

-- Description: Platform users with Role-Based Access Control (Admin, Hospital Admin, Researcher)

-- ------------------------------------------------------------------------------

CREATE TABLE users (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    institution_id UUID REFERENCES institutions(id) ON DELETE SET NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    full_name VARCHAR(255) NOT NULL,

    role user_role_enum NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    last_login TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: datasets

-- Description: Metadata registry of hospital-held datasets.

-- NOTE: Raw patient records remain strictly local to the hospital. Only schema and metadata are registered.

-- ------------------------------------------------------------------------------

CREATE TABLE datasets (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,

    name VARCHAR(255) NOT NULL,

    modality model_modality_enum NOT NULL DEFAULT 'tabular_ehr',

    sample_count INTEGER NOT NULL CHECK (sample_count >= 0),

    feature_schema JSONB NOT NULL DEFAULT '{}'::jsonb,

    is_validated BOOLEAN NOT NULL DEFAULT FALSE,

    privacy_budget_epsilon_spent DOUBLE PRECISION DEFAULT 0.0,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: fl_projects

-- Description: Collaborative study goals (e.g. Diabetic Retinopathy Detection, Sepsis Prediction)

-- ------------------------------------------------------------------------------

CREATE TABLE fl_projects (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(255) NOT NULL,

    description TEXT,

    target_condition VARCHAR(255) NOT NULL,

    model_architecture VARCHAR(100) NOT NULL, -- e.g. 'TabularMLP', 'ResNet18_Clinical'

    modality model_modality_enum NOT NULL,

    created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: fl_sessions

-- Description: Concrete Federated Learning training jobs/runs for an FL project

-- ------------------------------------------------------------------------------

CREATE TABLE fl_sessions (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL REFERENCES fl_projects(id) ON DELETE CASCADE,

    session_name VARCHAR(255) NOT NULL,

    total_rounds INTEGER NOT NULL DEFAULT 10 CHECK (total_rounds > 0),

    current_round INTEGER NOT NULL DEFAULT 0 CHECK (current_round >= 0),

    min_participating_clients INTEGER NOT NULL DEFAULT 2 CHECK (min_participating_clients >= 1),

    aggregation_strategy VARCHAR(50) NOT NULL DEFAULT 'FedAvg', -- FedAvg, FedProx

    dp_enabled BOOLEAN NOT NULL DEFAULT TRUE,

    dp_epsilon DOUBLE PRECISION NOT NULL DEFAULT 1.5,

    dp_delta DOUBLE PRECISION NOT NULL DEFAULT 1e-5,

    dp_max_grad_norm DOUBLE PRECISION NOT NULL DEFAULT 1.0,

    learning_rate DOUBLE PRECISION NOT NULL DEFAULT 0.001,

    local_epochs INTEGER NOT NULL DEFAULT 3 CHECK (local_epochs >= 1),

    batch_size INTEGER NOT NULL DEFAULT 32 CHECK (batch_size >= 1),

    status session_status_enum NOT NULL DEFAULT 'created',

    started_at TIMESTAMP WITH TIME ZONE,

    finished_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: fl_session_participants

-- Description: Association between FL sessions and participating hospitals

-- ------------------------------------------------------------------------------

CREATE TABLE fl_session_participants (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    session_id UUID NOT NULL REFERENCES fl_sessions(id) ON DELETE CASCADE,

    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,

    client_status client_status_enum NOT NULL DEFAULT 'registered',

    local_dataset_id UUID REFERENCES datasets(id) ON DELETE SET NULL,

    last_heartbeat TIMESTAMP WITH TIME ZONE,

    registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_session_institution UNIQUE (session_id, institution_id)

);



-- ------------------------------------------------------------------------------

-- TABLE: fl_round_metrics

-- Description: Aggregated global performance metrics recorded after each FedAvg round

-- ------------------------------------------------------------------------------

CREATE TABLE fl_round_metrics (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    session_id UUID NOT NULL REFERENCES fl_sessions(id) ON DELETE CASCADE,

    round_number INTEGER NOT NULL CHECK (round_number >= 0),

    global_loss DOUBLE PRECISION NOT NULL,

    global_accuracy DOUBLE PRECISION NOT NULL,

    global_auc DOUBLE PRECISION,

    global_f1_score DOUBLE PRECISION,

    global_precision DOUBLE PRECISION,

    global_recall DOUBLE PRECISION,

    participating_clients_count INTEGER NOT NULL,

    round_duration_seconds DOUBLE PRECISION,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_session_round UNIQUE (session_id, round_number)

);



-- ------------------------------------------------------------------------------

-- TABLE: fl_client_round_metrics

-- Description: Anonymized/local client metrics reported during round validation

-- ------------------------------------------------------------------------------

CREATE TABLE fl_client_round_metrics (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    round_metric_id UUID NOT NULL REFERENCES fl_round_metrics(id) ON DELETE CASCADE,

    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,

    local_loss DOUBLE PRECISION NOT NULL,

    local_accuracy DOUBLE PRECISION NOT NULL,

    local_samples_trained INTEGER NOT NULL CHECK (local_samples_trained > 0),

    local_training_duration_seconds DOUBLE PRECISION,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: model_checkpoints

-- Description: Global model weight artifacts stored securely per round

-- ------------------------------------------------------------------------------

CREATE TABLE model_checkpoints (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    session_id UUID NOT NULL REFERENCES fl_sessions(id) ON DELETE CASCADE,

    round_number INTEGER NOT NULL,

    file_path VARCHAR(500) NOT NULL,

    file_size_bytes BIGINT NOT NULL,

    sha256_checksum VARCHAR(64) NOT NULL,

    is_best_model BOOLEAN NOT NULL DEFAULT FALSE,

    metrics_summary JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- TABLE: audit_logs

-- Description: Immutable audit trail for HIPAA/GDPR regulatory compliance

-- ------------------------------------------------------------------------------

CREATE TABLE audit_logs (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id) ON DELETE SET NULL,

    institution_id UUID REFERENCES institutions(id) ON DELETE SET NULL,

    action VARCHAR(100) NOT NULL,             -- e.g., 'AUTH_LOGIN', 'START_FL_SESSION', 'DOWNLOAD_WEIGHTS'

    resource_type VARCHAR(100) NOT NULL,      -- e.g., 'FL_SESSION', 'USER', 'DATASET'

    resource_id VARCHAR(255),

    ip_address VARCHAR(45),

    user_agent TEXT,

    details JSONB DEFAULT '{}'::jsonb,

    status VARCHAR(50) NOT NULL DEFAULT 'SUCCESS', -- 'SUCCESS', 'FAILED', 'UNAUTHORIZED'

    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);



-- ------------------------------------------------------------------------------

-- INDEXES FOR QUERY OPTIMIZATION

-- ------------------------------------------------------------------------------

CREATE INDEX idx_users_email ON users(email);

CREATE INDEX idx_users_role ON users(role);

CREATE INDEX idx_users_institution ON users(institution_id);

CREATE INDEX idx_datasets_institution ON datasets(institution_id);

CREATE INDEX idx_fl_sessions_project ON fl_sessions(project_id);

CREATE INDEX idx_fl_sessions_status ON fl_sessions(status);

CREATE INDEX idx_fl_round_metrics_session_round ON fl_round_metrics(session_id, round_number);

CREATE INDEX idx_fl_client_round_metrics_round ON fl_client_round_metrics(round_metric_id);

CREATE INDEX idx_audit_logs_user_timestamp ON audit_logs(user_id, timestamp DESC);

CREATE INDEX idx_audit_logs_action ON audit_logs(action);
