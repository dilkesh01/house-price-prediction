
from pydantic import BaseModel, Field
from typing import Literal

Location = Literal["Gurugram", "Delhi", "Noida", "Sonipat", "Jaipur", "Bengaluru"]

class PredictionRequest(BaseModel):
    area_sqft: float = Field(gt=100, le=20000)
    bedrooms: int = Field(ge=1, le=10)
    bathrooms: int = Field(ge=1, le=10)
    property_age: int = Field(ge=0, le=100)
    location: Location
    parking: bool = False
    furnished: bool = False
