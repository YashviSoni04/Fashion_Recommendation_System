# 👗 Fashion Recommendation System

An AI-powered fashion recommendation system built using **FastAPI** and **Google Gemini**, with a responsive and elegant **HTML frontend UI**. Users can input personal style preferences and receive detailed outfit suggestions tailored to their body type, occasion, budget, and more.

---

## 🚀 Features

- ✅ Gemini 1.5 integration for intelligent outfit generation
- ✅ Stylish frontend UI (HTML + CSS + JS)
- ✅ Interactive Swagger API docs at `/docs`
- ✅ Health check endpoints
- ✅ Enum-driven input validation using Pydantic
- ✅ Error handling and structured responses
- ✅ Fully customizable and ready for deployment

---

## 🛠 Tech Stack

- **Backend**: FastAPI, Pydantic
- **AI**: Google Gemini via `google-generativeai`
- **Frontend**: HTML, CSS, JavaScript
- **Env Management**: python-dotenv
- **Logging & Validation**: logging, enums, schema examples

---

## 🧪 Live Endpoints

| Method | Endpoint           | Description                            |
|--------|--------------------|----------------------------------------|
| GET    | `/`                | Root health check                      |
| GET    | `/health`          | Full system + Gemini config check     |
| POST   | `/recommend`       | Get AI-generated outfit suggestions   |
| GET    | `/ui`              | HTML-based frontend                    |
| GET    | `/docs`            | Swagger UI for testing API            |
| GET    | `/redoc`           | Alternative auto-generated docs       |

---

## 🧰 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fashion-recommendation-api.git
cd fashion-recommendation-api


2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows

3. Install dependencies
pip install -r requirements.txt

4. Create .env file
GEMINI_API_KEY=your_real_api_key
ENVIRONMENT=development
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO


5. Run the API
python run.py


6. Visit the App
Frontend UI: http://localhost:8000/ui
API Documentation: http://localhost:8000/docs
Alternative Docs: http://localhost:8000/redoc
Health Check: http://localhost:8000/health

## 🌟 Frontend Preview

<img src="/assets/ui-preview.png" alt="Fashion Recommendation UI" width="100%" />
