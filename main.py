from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from fastapi.responses import FileResponse

from app.routes import auth, property, upload, reservation, task, stats, dashboard

app = FastAPI(
    title="Lelyo API",
    description="API officielle de Lelyo — plateforme de gestion de biens Airbnb, réservations et tâches.",
    version="1.0.0",
    contact={
        "name": "Sena DOMONHEDO",
        "email": "contact@lelyo.dev",
        "url": "https://lelyo.dev"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/favicon.ico")
def favicon():
    return FileResponse("uploads/favicon.ico")


@app.get("/")
def root():
    return {
        "project": "Lelyo API",
        "version": "1.0.0",
        "description": "API robuste pour la gestion de biens Airbnb, réservations et tâches.",
        "developer": {
            "name": "Sena DOMONHEDO",
            "email": "contact@lelyo.dev",
            "github": "https://github.com/senado-09",
            "website": "https://lelyo.dev"
        },
        "status": "✅ En ligne",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(property.router)
app.include_router(upload.router)
app.include_router(reservation.router)
app.include_router(task.router)
app.include_router(stats.router)
app.include_router(dashboard.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
