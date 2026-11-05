
from pydantic import BaseModel, Field, field_validator


class CustomerFeatures(BaseModel):

    # Numerical features
    tenure: int = Field(ge=0, description="Number of months the customer has stayed")
    monthlycharges: float = Field(ge=0, description="Monthly charges")
    totalcharges: float = Field(ge=0, description="Total charges")

    # Categorical features
    gender: str
    seniorcitizen: int = Field(ge=0, le=1)
    partner: str
    dependents: str
    phoneservice: str
    multiplelines: str
    internetservice: str
    onlinesecurity: str
    deviceprotection: str
    techsupport: str
    streamingtv: str
    streamingmovies: str
    contract: str
    paperlessbilling: str
    paymentmethod: str

    # Swagger UI example
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tenure": 12,
                    "monthlycharges": 70.5,
                    "totalcharges": 850,
                    "gender": "Female",
                    "seniorcitizen": 0,
                    "partner": "Yes",
                    "dependents": "No",
                    "phoneservice": "Yes",
                    "multiplelines": "No",
                    "internetservice": "Fiber optic",
                    "onlinesecurity": "No",
                    "deviceprotection": "Yes",
                    "techsupport": "No",
                    "streamingtv": "Yes",
                    "streamingmovies": "No",
                    "contract": "Month-to-month",
                    "paperlessbilling": "Yes",
                    "paymentmethod": "Bank transfer (automatic)"
                }
            ]
        }
    }

    # Normalize categorical values
    @field_validator(
        "gender", "partner", "dependents", "phoneservice",
        "multiplelines", "internetservice", "onlinesecurity",
        "deviceprotection", "techsupport", "streamingtv",
        "streamingmovies", "contract", "paperlessbilling",
        "paymentmethod",
        mode="before"
    )
    @classmethod
    def clean_categorical_values(cls, value):
        if isinstance(value, str):
            return value.strip().lower().replace(" ", "_")
        return value

    # Validate gender
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):
        if value not in ["female", "male"]:
            raise ValueError("Gender must be female or male")
        return value

    # Validate yes/no values
    @field_validator(
        "partner", "dependents", "phoneservice", "paperlessbilling"
    )
    @classmethod
    def validate_yes_no(cls, value):
        if value not in ["yes", "no"]:
            raise ValueError("Value must be yes or no")
        return value

    # Validate multiple lines
    @field_validator("multiplelines")
    @classmethod
    def validate_multiplelines(cls, value):
        if value not in ["yes", "no", "no_phone_service"]:
            raise ValueError("Invalid multiplelines value")
        return value

    # Validate internet service
    @field_validator("internetservice")
    @classmethod
    def validate_internetservice(cls, value):
        if value not in ["dsl", "fiber_optic", "no"]:
            raise ValueError("Invalid internetservice value")
        return value

    # Validate internet-related features
    @field_validator(
        "onlinesecurity", "deviceprotection", "techsupport",
        "streamingtv", "streamingmovies"
    )
    @classmethod
    def validate_internet_features(cls, value):
        if value not in ["yes", "no", "no_internet_service"]:
            raise ValueError("Invalid internet service feature value")
        return value

    # Validate contract
    @field_validator("contract")
    @classmethod
    def validate_contract(cls, value):
        if value not in ["month-to-month", "one_year", "two_year"]:
            raise ValueError("Invalid contract value")
        return value

    # Validate payment method
    @field_validator("paymentmethod")
    @classmethod
    def validate_paymentmethod(cls, value):
        allowed = [
            "bank_transfer_(automatic)",
            "credit_card_(automatic)",
            "electronic_check",
            "mailed_check"
        ]

        if value not in allowed:
            raise ValueError("Invalid payment method")

        return value
