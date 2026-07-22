# AD-CLICK-FRAUD-DETECTION-

## What this is
AD-CLICK-FRAUD-DETECTION- is a Django-based web application and research prototype for detecting fraudulent ad clicks and suspicious network flows. It provides both host/IP-level risk scoring (batch analysis) and real-time click-level fraud detection using pre-trained ML model bundles. The app is intended for security researchers and developers who want a runnable demo of feature extraction, model inference, and simple rule-based explanations alongside saved model artifacts and example data.

### Stack
- **Language(s):** Python (Django) primary; HTML, CSS, JavaScript for the web UI
- **Framework / runtime:** Django 5.2
- **Notable libraries:** pandas, numpy, scikit-learn (models), joblib/pickle for model bundles

## How it's organized
```
Cyber/                 Django project settings & WSGI/ASGI
Security/              Django app: views, models, forms, templates, static
manage.py              Django management entrypoint
db.sqlite3             Example SQLite database (development)
synthetic_flows.csv    Example flow dataset used for IP/host feature extraction
realtime_fraud_model.pkl  Saved model bundle for click-level real-time detection
risk_model.pkl         Saved model bundle for IP/host risk scoring
fraud_detection_model.pkl  Another model artifact (additional experiments)
README.md              This file (updated)
LICENSE                Project license
```

How it fits together: The Django project (Cyber) loads the Security app which exposes web views for: pasting a URL to predict whether an ad click is fraudulent (predict_link), pasting an IP to analyze flows and score risk (paste_ip), and a JSON endpoint for realtime click telemetry (realtime_click) which accepts client/server signals and returns a prediction. The views load pre-trained model bundles (pickle / joblib) from the repo root, align/encode features, and run model.predict / predict_proba. Rule-based heuristics in views provide human-readable reasons alongside model outputs.

## How to run it
1. Create a Python virtual environment and install dependencies. There is no requirements.txt in the repository, but the code uses Django, pandas, numpy, scikit-learn and joblib. For a minimal environment:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install django==5.2 pandas numpy scikit-learn joblib
```

2. Run migrations and start the development server (db.sqlite3 is already included):

```bash
python manage.py migrate
python manage.py createsuperuser   # optional: create admin user
python manage.py runserver
```

3. Open http://127.0.0.1:8000/ and use the UI pages:
- Home / index (views.home -> index.html)
- Paste a link: paste_link -> predict_link (form posts to predict_link view)
- Paste an IP: paste_ip (analyzes synthetic_flows.csv and scores with risk_model.pkl)
- Realtime endpoint: POST JSON to /realtime_click/ (view realtime_click) to get a JSON prediction

Notes:
- Model bundles are stored as pickle/joblib files at the repository root. They are expected to be dict bundles containing keys like `model`, `features`, `encoders`, and optionally `suspicious_list`.
- If you intend to retrain or re-generate models, re-save them following the same bundle layout used in views (dict with model, feature names, encoders).

## Data & artifacts
- synthetic_flows.csv — example CSV with timestamped flows used by the IP analysis view.
- db.sqlite3 — included development DB; remove before publishing if it contains sensitive data.
- *.pkl files — pre-trained model bundles used by the demo views. They may be large; keep them out of production repos or replace with a proper model registry in production.

## Try asking
- How do I add a new feature to the realtime model bundle (what files define the feature list)?
- Where in the code is the CSV parsing for `synthetic_flows.csv` done and what columns does it expect? (look at `Security/views.py` `_compute_host_features_for_ip`)
- Which template should I modify to change the paste-IP form and the IP results layout? (search for `paste_ip.html` in the templates directory)

---


