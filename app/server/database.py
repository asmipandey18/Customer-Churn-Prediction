from pymongo import AsyncMongoClient

# MongoDB connection URL
MONGO_URL = "mongodb://localhost:27017"

# Create MongoDB client
client = AsyncMongoClient(MONGO_URL)

# Select database
database = client["churn_prediction"]

# Select collection
prediction_collection = database["prediction_logs"]