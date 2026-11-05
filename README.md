# Customer Churn Prediction API

A Machine Learning-powered REST API that predicts whether a customer is likely to leave a company using a trained Logistic Regression model. Built with **FastAPI**, **Scikit-learn**, and **MongoDB**, this project provides customer churn predictions and stores prediction history for future reference.

## Project Overview

Customer churn is a major challenge for businesses because losing customers can negatively affect revenue and business growth.

This project uses historical telecom customer data to predict whether a customer is likely to discontinue a company's services.

Users can submit customer information through the API and receive:
- A binary churn prediction (`True` or `False`).
- A churn probability score.
- A unique prediction log ID.

Each prediction is automatically stored in MongoDB, where users can retrieve, view, and delete prediction records.

## Key Features

- Predict customer churn using a trained Machine Learning model.
- Validate input data using Pydantic.
- Generate churn predictions and probability scores.
- Store customer information and prediction results in MongoDB.
- Retrieve all prediction logs.
- Support pagination when retrieving logs.
- Retrieve an individual prediction using its ID.
- Delete individual prediction records.
- Interactive API documentation through Swagger UI.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API development |
| Uvicorn | ASGI server |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| Logistic Regression | Classification algorithm |
| DictVectorizer | Feature encoding |
| Pydantic | Input validation |
| MongoDB | Database |
| PyMongo | MongoDB integration |
| Pickle | Model serialization and loading |
| Docker | Running MongoDB |
| Git & GitHub | Version control |

## Machine Learning Model

This project uses a trained **Logistic Regression** classification model.

The model predicts whether a customer is likely to leave the company.

- `True`: Customer is predicted to churn.
- `False`: Customer is predicted not to churn.

### Model Features

The model uses 18 customer features.

**Numerical Features**
- `tenure`
- `monthlycharges`
- `totalcharges`

**Categorical Features**
- `gender`
- `seniorcitizen`
- `partner`
- `dependents`
- `phoneservice`
- `multiplelines`
- `internetservice`
- `onlinesecurity`
- `deviceprotection`
- `techsupport`
- `streamingtv`
- `streamingmovies`
- `contract`
- `paperlessbilling`
- `paymentmethod`

The trained model and DictVectorizer are saved together in `churn_model.bin`.

The API loads the saved model when the application starts. It transforms customer input into numerical features and generates a churn probability.

A probability threshold of `0.5` is used to determine the final prediction.

## Project Structure

```text
Customer-Churn-Prediction/
│
├── app/
│   ├── __init__.py
│   └── server/
│       ├── __init__.py
│       ├── app.py
│       ├── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── prediction.py
│       └── routes/
│           ├── __init__.py
│           └── prediction.py
│
├── churn_model.bin
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/asmipandey18/Customer-Churn-Prediction.git
```

### 2. Navigate to the Project Directory

```bash
cd Customer-Churn-Prediction
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows using Git Bash:

```bash
source venv/Scripts/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start MongoDB Using Docker

Make sure Docker Desktop is running.

Create and start the MongoDB container:

```bash
docker run -d --name mongodb -p 27017:27017 mongo:5.0.6
```

If the container already exists, start it using:

```bash
docker start mongodb
```

### 6. Run the FastAPI Application

From the project root directory:

```bash
uvicorn app.server.app:app --reload
```

The API will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI provides interactive documentation through Swagger UI.

Open:

http://127.0.0.1:8000/docs

You can test all API endpoints directly from your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| POST | `/predict` | Predict customer churn and save the result |
| GET | `/logs` | Retrieve all prediction logs |
| GET | `/logs/{log_id}` | Retrieve a specific prediction log |
| DELETE | `/logs/{log_id}` | Delete a prediction log |

### 1. Predict Customer Churn

**Method:** POST

**Endpoint:** `/predict`

Submit customer information to receive a churn prediction.

Example request:

```json
{
    "tenure": 12,
    "monthlycharges": 70.5,
    "totalcharges": 850,
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "yes",
    "multiplelines": "no",
    "internetservice": "fiber_optic",
    "onlinesecurity": "no",
    "deviceprotection": "yes",
    "techsupport": "no",
    "streamingtv": "yes",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check"
}
```

Example response:

```json
{
    "log_id": "YOUR_GENERATED_LOG_ID",
    "churn_prediction": true,
    "confidence_score": 0.5746
}
```

The prediction result and customer information are automatically stored in MongoDB.

### 2. Get All Prediction Logs

**Method:** GET

**Endpoint:** `/logs`

Retrieves stored prediction records.

Supports pagination through query parameters:

- `skip`: Number of records to skip.
- `limit`: Maximum number of records to retrieve.

Example:

```text
GET /logs?skip=0&limit=10
```

### 3. Get a Prediction by ID

**Method:** GET

**Endpoint:** `/logs/{log_id}`

Retrieves a specific prediction record using its MongoDB ObjectId.

Returns an error if the ID is invalid or the record does not exist.

### 4. Delete a Prediction Log

**Method:** DELETE

**Endpoint:** `/logs/{log_id}`

Deletes a specific prediction record from MongoDB.

Returns a success message if the record is deleted successfully.

## MongoDB Database

MongoDB is used to store prediction history.

**Database Name:** `churn_prediction`

**Collection Name:** `prediction_logs`

Each stored document contains:

- Customer input features.
- Churn prediction (`True` or `False`).
- Confidence score.
- Prediction timestamp.

## Future Improvements

- Develop an interactive frontend dashboard.
- Add user authentication and authorization.
- Improve model performance through hyperparameter tuning.
- Add prediction analytics and visualizations.
- Deploy the API to a cloud platform.

## Author

**Asmi Pandey**

GitHub: [@asmipandey18](https://github.com/asmipandey18)

**Project Repository:** [Customer Churn Prediction API](https://github.com/asmipandey18/Customer-Churn-Prediction)

---

Thank you for visiting this repository! Feedback and suggestions are always welcome.