# 📦 RetailForecast — Demand Forecasting for Small Retail Stores

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
  <b>"Predict demand, plan smarter."</b>
</p>

---

## 🖥️ Preview

<p align="center">
  <img width="975" height="449" alt="image" src="https://github.com/user-attachments/assets/858b7ef2-1c30-475f-8df8-15ca64ba5696" />

</p>

---

## 🧠 About the Project

Small retail stores often struggle with inventory management — ordering too much leads to waste, while ordering too little results in lost sales. **RetailForecast** solves that problem by using machine learning models trained on historical sales data to accurately predict future product demand.

The system combines:
- **Python + Django** — Backend, ML pipeline, and REST API
- **React.js** — Modern, responsive web frontend
- **scikit-learn** — Machine learning for demand prediction

---

## ✨ Features

- 🔐 **Secure Authentication** — Login, logout, and forgot password support
- 📊 **Sales Data Management** — Upload and manage historical sales records
- 🤖 **ML-Powered Demand Forecasting** — Predict future stock needs automatically
- 📈 **Visual Analytics** — Charts showing trends, forecasts, and performance
- 🛒 **Inventory Optimization** — Smart recommendations to balance stock levels
- 🔔 **Reorder Alerts** — Get notified before products run out
- 🗂️ **Product & Category Management** — Manage your full product catalog
- 🌐 **Web Dashboard** — Clean, user-friendly React interface

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Django 4.x | Web framework |
| Django REST Framework | REST API |
| scikit-learn | ML models |
| pandas / NumPy | Data processing |
| Matplotlib | Data visualization |

### Frontend
| Technology | Purpose |
|---|---|
| React.js 18.x | Web frontend framework |
| JavaScript (ES6+) | Programming language |
| Axios / Fetch API | API communication |
| CSS3 / Tailwind | Styling & UI |
| Recharts / Chart.js | Data charts |

### Database
| Technology | Purpose |
|---|---|
| SQLite | Local development |
| PostgreSQL | Production database |

---

## 📁 Project Structure

```
Demand_forcasting/
│
├── backend/                        # Django backend
│   ├── demand_forecasting/         # Main Django project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── forecasting/                # Core app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── ml/                     # ML pipeline
│   │       ├── train.py
│   │       ├── predict.py
│   │       └── preprocess.py
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                       # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Page-level components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Forecast.jsx
│   │   │   └── Inventory.jsx
│   │   ├── services/               # API calls
│   │   ├── context/                # State management
│   │   └── App.jsx
│   ├── package.json
│   └── .env
│
├── screenshots/
│   └── login.png
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

---

### 🔧 Backend Setup (Django)

```bash
# 1. Clone the repository
git clone https://github.com/Aswathyvk/Demand_forecasting.git
cd Demand_forecasting/backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000/`

---

### 🌐 Frontend Setup 

```bash
# Navigate to the frontend folder
cd ../frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend runs at: `http://localhost:1235/` (or default `http://localhost:3000/`)

> **Note:** Set your Django API URL in the `.env` file:
> ```
> REACT_APP_API_URL=http://127.0.0.1:8000/api
> ```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/forgot-password/` | Password reset |
| GET | `/api/products/` | List all products |
| POST | `/api/sales/upload/` | Upload sales CSV |
| GET | `/api/forecast/<product_id>/` | Get demand forecast |
| GET | `/api/inventory/alerts/` | Get reorder alerts |
| GET | `/api/analytics/trends/` | Sales trend data |

---

## 🤖 Machine Learning Models

The system uses these ML approaches for demand prediction:

- **Linear Regression** — Baseline forecasting
- **Random Forest Regressor** — Captures non-linear patterns
- **ARIMA / SARIMA** — Time-series with seasonality support
- **Feature Engineering** — Day of week, month, holidays, promotions

Models are retrained as new sales data is added.

---

## 📸 Screenshots

| Login | Dashboard | Forecast |
|-------|-----------|----------|
| [Login]<img width="930" height="1138" alt="image" src="https://github.com/user-attachments/assets/ee7294e9-b3cb-40cd-b68c-1b23bc2750f5" /> | [Dashboard]<img width="922" height="1165" alt="image" src="https://github.com/user-attachments/assets/e961f383-d87e-48af-aee7-0736f60f3666" />
 | [Forecast]<img width="934" height="1184" alt="image" src="https://github.com/user-attachments/assets/dd7b3dfd-b5af-4527-b957-b9d4d70a342f" />
 

---

## 👩‍💻 Author

**Aswathy VK**
- GitHub: [@Aswathyvk](https://github.com/Aswathyvk)

---

<p align="center">
  © 2026 RetailForecast. All rights reserved. <br/>
  <i>Predict demand, plan smarter.</i>
</p>
