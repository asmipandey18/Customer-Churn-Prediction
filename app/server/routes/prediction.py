
from datetime import datetime, timezone
from fastapi import APIRouter, Request, Query, HTTPException
from bson import ObjectId
from app.server.database import prediction_collection
from app.server.models.prediction import CustomerFeatures

router = APIRouter()


@router.post("/predict")
async def predict_churn(customer: CustomerFeatures, request: Request):

    # Convert customer data into a dictionary
    customer_data = customer.model_dump()

    # Get the trained model and vectorizer
    dv = request.app.state.dv
    model = request.app.state.model

    # Convert customer data into numerical features
    X = dv.transform([customer_data])

    # Predict churn probability
    probability = float(model.predict_proba(X)[0, 1])

    # Determine churn prediction
    prediction = probability >= 0.5

    # Prepare prediction log
    log_data = {
        "features": customer_data,
        "churn_prediction": prediction,
        "confidence_score": probability,
        "timestamp": datetime.now(timezone.utc)
    }

    # Save prediction in MongoDB
    result = await prediction_collection.insert_one(log_data)

    return {
        "log_id": str(result.inserted_id),
        "churn_prediction": prediction,
        "confidence_score": probability
    }

@router.get("/logs")
async def get_prediction_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    # Retrieve prediction logs from MongoDB
    logs = await prediction_collection.find().skip(skip).limit(limit).to_list(length=limit)

    # Convert MongoDB ObjectId into string
    for log in logs:
        log["_id"] = str(log["_id"])

    # Count total prediction records
    total = await prediction_collection.count_documents({})

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "logs": logs
    }


@router.get("/logs/{log_id}")
async def get_prediction_log(log_id: str):

    # Check whether the ID is a valid MongoDB ObjectId
    if not ObjectId.is_valid(log_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid prediction log ID"
        )

    # Find the prediction record in MongoDB
    log = await prediction_collection.find_one(
        {"_id": ObjectId(log_id)}
    )

    # Check whether the record exists
    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction log not found"
        )

    # Convert ObjectId into string
    log["_id"] = str(log["_id"])

    return log

@router.delete("/logs/{log_id}")
async def delete_prediction_log(log_id: str):

    # Check whether the ID is valid
    if not ObjectId.is_valid(log_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid prediction log ID"
        )

    # Delete the prediction record
    result = await prediction_collection.delete_one(
        {"_id": ObjectId(log_id)}
    )

    # Check whether the record exists
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Prediction log not found"
        )

    return {
        "message": "Prediction log deleted successfully",
        "log_id": log_id
    }