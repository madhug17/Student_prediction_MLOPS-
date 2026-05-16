# 🎓 Student Performance Prediction - End-to-End MLOps Platform

##  Overview
This repository hosts a production-grade, asynchronous end-to-end MLOps platform engineered to predict student academic outcomes. Built using a decoupling architecture, the system separates high-compute model inferences from the web server using an asynchronous task worker queue, ensuring scalable and resilient real-time streaming operations.

The complete ML application lifecycle handles:
* **Secure API Access:** Token-based security gating prediction requests.
* **Asynchronous Task Processing:** Distributed worker architecture managing computation loads.
* **Feature Management & Explainability:** Feature preparation tracked alongside localized model interpretations (SHAP).
* **Automated CI/CD Workflows:** Automated regression test sessions, multi-platform Docker compilations, and seamless continuous delivery.
* **Production Observability:** Native Prometheus engine scraping live server latency, uptime rates, and runtime diagnostics.

---

##  System Architecture

```text
       [ Live Python Client / cURL Call ]
                       │
                       ▼ (OAuth2 Token Handshake)
         [ FastAPI Inference API ]
                       │
         ┌─────────────┴─────────────┐
         ▼ (rpush Task Payload)      ▼ (Scrapes Runtime Metrics)
   [ Redis Cloud Queue ]      [ Prometheus Service Core ]
         │                           │
         ▼ (Pops Worker Tasks)       ▼ (Binds Observability Matrix)
  [ Distributed Celery ]      [ Grafana UI Monitoring Dashboard ]
         │
         ▼ (Executes Joblib File Inference)
 [ Scikit-Learn Regression Model ]


Student_prediction_MLOPS-/
│
├── .github/workflows/   # Automated CI/CD execution pipeline files
├── models/              # Serialized binary machine learning model weights (.joblib)
├── venv/                # Local runtime python virtual environment cache 
├── app01.py             # Core FastAPI web server entrypoint script
├── tasks.py             # Asynchronous distributed Celery processing logic
├── test_api.py          # Pipeline regression testing orchestration files
├── test_live_api.py     # Production validation consumer user script
├── requirements.txt     # Locked application library dependencies file
├── Dockerfile           # Optimized production multi-stage build manifest
└── README.md            # Technical architecture dossier documentation
