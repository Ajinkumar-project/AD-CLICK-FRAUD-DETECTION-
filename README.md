<div align="center">

# 🛡️ AD Click Fraud Detection

### AI-Powered Ad Click Fraud Detection & Network Risk Analysis

Detect fraudulent advertisement clicks and suspicious network activity using Machine Learning and Django.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

![GitHub Repo stars](https://img.shields.io/github/stars/Ajinkumar-project/AD-CLICK-FRAUD-DETECTION-?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/Ajinkumar-project/AD-CLICK-FRAUD-DETECTION-?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/Ajinkumar-project/AD-CLICK-FRAUD-DETECTION-?style=flat-square)
![GitHub license](https://img.shields.io/github/license/Ajinkumar-project/AD-CLICK-FRAUD-DETECTION-?style=flat-square)

</div>

---

# 📖 Overview

**AD Click Fraud Detection** is a Machine Learning-powered Django web application that detects fraudulent advertisement clicks and suspicious network traffic.

The system combines **AI-based prediction** with **rule-based analysis** to identify malicious clicks, analyze IP behavior, and calculate risk scores using pre-trained machine learning models.

---

# ✨ Features

- 🔍 URL Fraud Detection
- 🌐 IP Risk Analysis
- 🤖 Machine Learning Predictions
- ⚡ Real-time Click Detection API
- 📊 Host/IP Risk Scoring
- 📈 Probability Score
- 🛡️ Rule-Based Explanations
- 📁 Batch Flow Analysis
- 💾 Pre-trained ML Models
- 📱 Responsive Web Interface

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | Django 5.2 |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib, Pickle |

---

# 📂 Project Structure

```text
Cyber/
│
├── Cyber/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── Security/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── urls.py
│
├── synthetic_flows.csv
├── realtime_fraud_model.pkl
├── risk_model.pkl
├── fraud_detection_model.pkl
├── db.sqlite3
├── manage.py
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Ajinkumar-project/AD-CLICK-FRAUD-DETECTION-.git
```

Move into the project

```bash
cd AD-CLICK-FRAUD-DETECTION-
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install django pandas numpy scikit-learn joblib
```

Run migrations

```bash
python manage.py migrate
```

Start the server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---

# 🚀 Application Modules

### 🏠 Home

Landing page of the application.

### 🔗 URL Fraud Detection

Paste an advertisement URL to determine whether it is fraudulent.

### 🌐 IP Risk Analyzer

Analyze suspicious IP addresses using historical network flow data.

### ⚡ Real-Time Detection

REST API endpoint that predicts fraud from live click telemetry.

### 📊 Risk Score

Displays

- Fraud Probability
- Risk Level
- Suspicious Indicators
- AI Prediction

---

# 📦 Model Files

| File | Purpose |
|------|---------|
| realtime_fraud_model.pkl | Live click detection |
| risk_model.pkl | Host/IP risk scoring |
| fraud_detection_model.pkl | Experimental model |
| synthetic_flows.csv | Sample network flow dataset |

---

# 📸 Screenshots

> Add screenshots here

```
Home Page

URL Prediction

IP Analysis

Dashboard

Prediction Result
```

---

# 🔮 Future Improvements

- Deep Learning Model
- Explainable AI (XAI)
- Live Dashboard
- Docker Support
- REST API Authentication
- PostgreSQL Support
- Cloud Deployment
- User Login System

---

# 🤝 Contributing

Contributions are welcome.

Fork the repository

```bash
git checkout -b feature/NewFeature
```

Commit changes

```bash
git commit -m "Added New Feature"
```

Push

```bash
git push origin feature/NewFeature
```

Create a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you found this project helpful, please give it a Star!

Made with ❤️ using Django & Machine Learning

</div>
