# Machine Learning Module: Clinical Models & Healthcare Data Pipeline



## Overview

This module contains the deep learning and machine learning models implemented in **PyTorch**, clinical data preprocessing pipelines, synthetic EHR generation tools, and clinical evaluation metrics.



## Directory Structure

- `models/`: PyTorch neural network architectures:

  - `tabular_net.py`: Multilayer Perceptron (MLP) with Batch Normalization and Dropout for clinical EHR risk prediction (e.g. cardiovascular disease / diabetes onset).

  - `cnn_classifier.py`: Lightweight Convolutional Neural Network designed for medical image classification (e.g., chest X-ray binary/multiclass detection).

- `datasets/`: Healthcare dataset loaders & generation scripts:

  - `synthetic_ehr.py`: Generator for realistic synthetic Electronic Health Records (demographics, vital signs, lab values, diagnostic outcomes) ensuring zero real PII risk during testing.

  - `data_loader.py`: Train/Validation/Test data splitting, PyTorch DataLoader creation, and batching.

- `preprocessing/`: Clinical feature standardization, missing value handling, and categorical encoding.

- `evaluation/`: Clinical evaluation metrics suite:

  - ROC-AUC (Area Under Receiver Operating Characteristic)

  - PR-AUC (Precision-Recall Curve)

  - Sensitivity / Recall & Specificity

  - F1-Score & Confusion Matrix generation
