
from django.shortcuts import render
import pandas as pd
import pickle
import os
from django.conf import settings

def home(request):
    return render(request,"index.html")
# detector/views.py
from django.shortcuts import render
from django.conf import settings
import os, pickle
from urllib.parse import urlparse, parse_qs
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(settings.BASE_DIR,  "realtime_fraud_model.pkl")

def extract_url_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path_len = len(parsed.path)
    qs = parse_qs(parsed.query)
    num_params = len(qs)
    has_utm = int(any(k.startswith("utm") for k in qs.keys()))
    return {"domain": domain, "path_len": path_len, "num_params": num_params, "has_utm": has_utm}

def load_bundle():
    with open(MODEL_PATH, "rb") as f:
        data = pickle.load(f)
    if not isinstance(data, dict):
        raise ValueError("Loaded model file is not a dictionary bundle.")
    return data


def paste_link(request):
    return render(request, "paste_link.html")
import numpy as np
import pickle
from django.shortcuts import render
import numpy as np
import pandas as pd
import pickle
from django.shortcuts import render

def predict_link(request):
    context = {}
    if request.method == "POST":
        try:
            def _as_int(value, default=0):
                try:
                    return int(float(value))
                except (TypeError, ValueError):
                    return default

            def _as_float(value, default=0.0):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return default

            # Load model bundle
            with open("realtime_fraud_model.pkl", "rb") as f:
                bundle = pickle.load(f)

            if not isinstance(bundle, dict):
                raise ValueError("Loaded model file is not a dictionary bundle.")

            model = bundle['model']
            encoders = bundle.get('encoders', {})
            feature_columns = bundle.get('features', [])
            suspicious_list = set(bundle.get("suspicious_list", []))

            # Get inputs from form
            url = request.POST.get("url", "").strip()
            referrer = request.POST.get("referrer", "").strip() or "none"
            user_agent = request.POST.get("user_agent", "").strip() or "unknown"
            ip_address = request.POST.get("ip_address", "").strip() or "0.0.0.0"

            click_count_raw = request.POST.get("click_count", "").strip()
            click_interval_raw = request.POST.get("click_interval", "").strip()
            click_count = _as_int(click_count_raw, 1) if click_count_raw else 1
            click_interval = _as_float(click_interval_raw, 0.5) if click_interval_raw else 0.5

            url_features = extract_url_features(url) if url else {
                "domain": "",
                "path_len": 0,
                "num_params": 0,
                "has_utm": 0,
            }
            suspicious_domain = int(url_features["domain"] in suspicious_list) if url_features["domain"] else 0

            # Numeric features (fill defaults if missing)
            bytes_sent = _as_float(request.POST.get("bytes_sent", 0), 0.0)
            bytes_received = _as_float(request.POST.get("bytes_received", 0), 0.0)
            duration = _as_float(request.POST.get("duration", 0), 0.0)

            # Build row dict using model feature names
            row = {
                "domain": url_features["domain"],
                "path_len": int(url_features["path_len"]),
                "num_params": int(url_features["num_params"]),
                "has_utm": int(url_features["has_utm"]),
                "suspicious_domain": suspicious_domain,
                "ip_address": ip_address,
                "referrer": referrer,
                "user_agent": user_agent,
                "click_interval": click_interval,
                "click_count": click_count,
                "country": request.POST.get("country", "").strip() or "unknown",
                "device": request.POST.get("device", "").strip() or "unknown",
                "bytes_sent": bytes_sent,
                "bytes_received": bytes_received,
                "duration": duration,
            }

            # Encode categorical columns safely
            for col in feature_columns:
                if col not in row:
                    row[col] = 0
                elif col in encoders:
                    le = encoders[col]
                    try:
                        row[col] = int(le.transform([row[col]])[0])
                    except Exception:
                        row[col] = -1  # unseen category

            # Convert row to DataFrame with correct column order
            X_pred = pd.DataFrame([row], columns=feature_columns)
            X_pred = X_pred.fillna(0)

            # Predict
            pred_label = model.predict(X_pred)[0]
            proba = model.predict_proba(X_pred)[0][1] if hasattr(model, "predict_proba") else None

            # Build rule-based reasons
            reasons = []
            if row.get("suspicious_domain", 0) == 1:
                reasons.append("Domain known for shady click farms / suspicious domains.")
            if click_interval < 0.5 or click_count > 50:
                reasons.append("Clicks are extremely frequent (short interval or very high click count).")
            if user_agent.lower().startswith("python") or "bot" in user_agent.lower() or "adsbot" in user_agent.lower() or "curl" in user_agent.lower():
                reasons.append("User agent looks like a bot or crawler.")
            if referrer in ("", "none") or referrer.strip() == "":
                reasons.append("No referrer (direct traffic) - sometimes suspicious for automated clicks.")
            if not reasons:
                reasons.append("No obvious rule-based red flags - looks like a normal ad click.")

            # Prepare context for template
            context.update({
                "url": url,
                "prediction": "Fraudulent" if pred_label == 1 else "Legitimate",
                "probability": round(float(proba)*100, 2) if proba is not None else None,
                "reasons": reasons,
                "features": row
            })

        except Exception as e:
            context['error'] = str(e)

    return render(request, "predict_link.html", context)




# detector/views.py
from django.shortcuts import render
from django.conf import settings
import os, joblib, pandas as pd, numpy as np
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import SignupForm
from django.contrib.auth import logout

# Paths
DATA_CSV = os.path.join(settings.BASE_DIR, "synthetic_flows.csv")
MODEL_PATH = os.path.join(settings.BASE_DIR,  "risk_model.pkl")

# Load model once
MODEL_BUNDLE = None
def load_model():
    global MODEL_BUNDLE
    if MODEL_BUNDLE is None:
        MODEL_BUNDLE = joblib.load(MODEL_PATH)
    return MODEL_BUNDLE

# Helper: extract features and timeline for a single IP
def _compute_host_features_for_ip(ip):
    if not os.path.exists(DATA_CSV):
        return None, "Data file not found: " + DATA_CSV
    df = pd.read_csv(DATA_CSV, parse_dates=['timestamp'])
    df_ip = df[df['src_ip'] == ip].copy()
    if df_ip.empty:
        return None, "No flows found for IP: " + ip

    # Timeline aggregation
    df_ip['minute'] = df_ip['timestamp'].dt.floor('1min')
    timeline = df_ip.groupby('minute').agg(flows=('timestamp','count')).reset_index()

    # Feature extraction
    features = {
        'flows_roll': int(df_ip['timestamp'].count()),
        'bytes_roll': int(df_ip['bytes'].sum()),
        'ports_roll': int(df_ip['dst_port'].nunique()),
        'peers_roll': int(df_ip['dst_ip'].nunique()),
        'rst_count': int(df_ip['flags'].str.contains('R').sum())
    }

    return (features, timeline), None

# Main view
def paste_ip(request):
    context = {}
    if request.method == "POST":
        ip = request.POST.get('ip_address', '').strip()
        if not ip:
            context['error'] = "Please enter an IP address."
            return render(request, 'paste_ip.html', context)

        data, err = _compute_host_features_for_ip(ip)
        if err:
            context['error'] = err
            return render(request, 'paste_ip.html', context)

        features, timeline = data
        bundle = load_model()
        model = bundle['model']
        feature_cols = bundle['feature_cols']
        x = [features[c] for c in feature_cols]

        # Safe predict_proba
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([x])
            if probs.shape[1] == 1:
                if model.classes_[0] == 0:
                    prob = 0.0
                else:
                    prob = 100.0
            else:
                prob = float(probs[0][1] * 100)
        else:
            prob = None

        # Prediction
        pred = model.predict([x])[0]
        prediction = 'Risk' if pred == 1 else 'No Risk'

        # Rule-based reasons
        reasons = []
        if features['flows_roll'] > 200:
            reasons.append("Very high flow count from this IP.")
        if features['rst_count'] > 10:
            reasons.append("Many reset flags observed (possible scanning / failed attempts).")
        if features['ports_roll'] > 20:
            reasons.append("Communication observed to many destination ports (possible scanning).")
        if not reasons:
            reasons.append("No strong rule-based red flags — host looks normal.")

        # Feature importances
        importances = model.feature_importances_
        top_idx = np.argsort(importances)[::-1][:3]
        fi = [(feature_cols[i], float(importances[i]*100)) for i in top_idx]

        context.update({
            'ip': ip,
            'features': features,
            'probability': round(prob,2) if prob is not None else None,
            'prediction': prediction,
            'reasons': reasons,
            'feature_importances': fi,
            'timeline': timeline.to_dict(orient='records')
        })

    return render(request, 'paste_ip.html', context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


# Phase-2: Real-time click fraud detection (client + server signals + incremental learning)
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

REALTIME_MODEL_PATH = os.path.join(settings.BASE_DIR, "realtime_fraud_model.pkl")
_REALTIME_BUNDLE = None

def _load_realtime_bundle():
    global _REALTIME_BUNDLE
    if _REALTIME_BUNDLE is None:
        with open(REALTIME_MODEL_PATH, "rb") as f:
            _REALTIME_BUNDLE = pickle.load(f)
    if not isinstance(_REALTIME_BUNDLE, dict):
        raise ValueError("Realtime model bundle is not a dictionary.")
    return _REALTIME_BUNDLE

def _build_realtime_features(payload):
    def _as_int(value, default=0):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default

    def _as_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    client = payload.get("client", {}) or {}
    server = payload.get("server", {}) or {}

    # Client-side behavior signals
    features = {
        "click_count": _as_int(client.get("click_count", 1), 1),
        "click_interval": _as_float(client.get("click_interval", 0.5), 0.5),
        "scroll_depth": _as_float(client.get("scroll_depth", 0), 0.0),
        "mouse_moves": _as_int(client.get("mouse_moves", 0), 0),
        "key_presses": _as_int(client.get("key_presses", 0), 0),
        "time_on_page": _as_float(client.get("time_on_page", 0), 0.0),
        "viewport_w": _as_int(client.get("viewport_w", 0), 0),
        "viewport_h": _as_int(client.get("viewport_h", 0), 0),
        "is_headless": _as_int(client.get("is_headless", 0), 0),
    }

    # Server-side log signals
    features.update({
        "ua": str(server.get("user_agent", client.get("user_agent", "unknown"))),
        "ref": str(server.get("referrer", client.get("referrer", "none"))),
        "bytes_sent": _as_float(server.get("bytes_sent", 0), 0.0),
        "bytes_received": _as_float(server.get("bytes_received", 0), 0.0),
        "duration": _as_float(server.get("duration", 0), 0.0),
        "suspicious_domain": _as_int(server.get("suspicious_domain", 0), 0),
        "ip": str(server.get("ip", "")),
        "asn": str(server.get("asn", "")),
        "country": str(server.get("country", "")),
        "timestamp": str(server.get("timestamp", datetime.utcnow().isoformat())),
    })

    return features

def _encode_and_align(features, feature_columns, encoders):
    row = dict(features)
    for col in feature_columns:
        if col not in row:
            row[col] = 0
        elif col in encoders:
            le = encoders[col]
            try:
                row[col] = int(le.transform([row[col]])[0])
            except Exception:
                row[col] = -1
    X = pd.DataFrame([row], columns=feature_columns).fillna(0)
    return row, X

@csrf_exempt
def realtime_click(request):
    if request.method == "GET":
        return render(request, "realtime_click_test.html")
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON payload")

    try:
        bundle = _load_realtime_bundle()
        model = bundle["model"]
        encoders = bundle.get("encoders", {})
        feature_columns = bundle.get("features", [])

        features = _build_realtime_features(payload)
        row, X = _encode_and_align(features, feature_columns, encoders)

        pred_label = int(model.predict(X)[0])
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(X)[0][1])

        # Optional incremental learning if label provided
        label = payload.get("label", None)
        updated = False
        if label is not None and hasattr(model, "partial_fit"):
            y = np.array([int(label)])
            if not hasattr(model, "classes_"):
                model.partial_fit(X, y, classes=np.array([0, 1]))
            else:
                model.partial_fit(X, y)
            bundle["model"] = model
            with open(REALTIME_MODEL_PATH, "wb") as f:
                pickle.dump(bundle, f)
            updated = True

        return JsonResponse({
            "prediction": "Fraudulent" if pred_label == 1 else "Legitimate",
            "probability": round(proba * 100, 2) if proba is not None else None,
            "features": row,
            "model_updated": updated
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def realtime_click_test(request):
    return render(request, "realtime_click_test.html")


def complaint_register(request):
    from .forms import ComplaintForm

    success = False
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            form = ComplaintForm()
            success = True
    else:
        form = ComplaintForm()

    return render(request, "complaint_register.html", {"form": form, "success": success})


def complaint_list(request):
    from .models import Complaint

    complaints = Complaint.objects.all()
    return render(request, "complaint_list.html", {"complaints": complaints})


def logout_view(request):
    logout(request)
    return redirect("login")

