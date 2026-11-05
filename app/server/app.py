
import pickle
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.server.routes.prediction import router as prediction_router

from app.server.database import client


# Find the project root directory
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "churn_model.bin"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    await client.admin.command("ping")
    print("MongoDB connected successfully!")

    # Load the trained ML model
    with open(MODEL_PATH, "rb") as file:
        dv, model = pickle.load(file)

    app.state.dv = dv
    app.state.model = model

    print("Churn model loaded successfully!")

    yield

    # Application shutdown
    await client.close()
    print("MongoDB connection closed!")


app = FastAPI(lifespan=lifespan)
app.include_router(prediction_router)


@app.get("/")
async def home():
    return {"message": "Welcome to Customer Churn Prediction API"}
