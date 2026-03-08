from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers.trips import router as trips_router
from routers.offers import router as offers_router
from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.payments import router as payments_router
from routers.reservations import router as reservations_router
from routers.reviews import router as reviews_router
from routers.notifications import router as notifications_router
from routers.admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Carpooling API",
    description="A modern carpooling platform with price negotiation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(trips_router)
app.include_router(offers_router)
app.include_router(users_router)
app.include_router(payments_router)
app.include_router(reservations_router)
app.include_router(reviews_router)
app.include_router(notifications_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Carpooling API",
        "version": "2.0.0",
        "docs": "/docs"
    }