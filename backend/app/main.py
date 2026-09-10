from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.employees import router as employees_router
from app.routers.departments import router as departments_router
from app.routers.roles import router as roles_router
from app.routers.shifts import router as shifts_router
from app.routers.attendance import router as attendance_router
from app.routers.leaves import router as leaves_router
from app.routers.payroll import router as payroll_router
from app.routers.notifications import router as notifications_router
from app.routers.chat import router as chat_router
from app.routers.documents import router as documents_router
from app.routers.analytics import router as analytics_router
from app.routers.datasets import router as datasets_router
from app.routers.prediction import router as prediction_router
from app.routers.model_training import router as model_training_router
from app.routers.risk import router as risk_router
from app.routers.forecast import router as forecast_router
from app.routers.attrition_analytics import router as attrition_analytics_router
from app.routers.interventions import router as interventions_router
from app.routers.alerts import router as alerts_router
from app.websocket.workforce_ws import router as workforce_ws_router
from app.routers.reports import router as reports_router
from app.routers.audit_logs import router as audit_logs_router
from app.routers.tasks import router as tasks_router
from app.routers.performance_reviews import router as performance_reviews_router
from app.routers.ai_recommendations import router as ai_recommendations_router
from app.routers.search import router as search_router


app = FastAPI(
    title="WorkForce AI Pro",
    description="HR Attrition Prediction & Workforce Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(departments_router)
app.include_router(roles_router)
app.include_router(shifts_router)
app.include_router(attendance_router)
app.include_router(leaves_router)
app.include_router(payroll_router)
app.include_router(notifications_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(analytics_router)
app.include_router(datasets_router)
app.include_router(prediction_router)
app.include_router(model_training_router)
app.include_router(risk_router)
app.include_router(forecast_router)
app.include_router(attrition_analytics_router)
app.include_router(interventions_router)
app.include_router(alerts_router)
app.include_router(workforce_ws_router)
app.include_router(reports_router)
app.include_router(audit_logs_router)
app.include_router(tasks_router)
app.include_router(performance_reviews_router)
app.include_router(ai_recommendations_router)
app.include_router(search_router)


@app.get("/")
def root():
    return {
        "message": "WorkForce AI Pro API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }