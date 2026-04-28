from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    N: float = Field(..., ge=0, le=200, description="Nitrogen (mg/kg)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus (mg/kg)")
    K: float = Field(..., ge=0, le=250, description="Potassium (mg/kg)")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature (C)")
    humidity: float = Field(..., ge=0, le=100, description="Humidity (%)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH")
    rainfall: float = Field(..., ge=0, le=500, description="Rainfall (mm)")


class PredictResponse(BaseModel):
    crop: str
    confidence: float
    uncertainty: float
    validation_hint: str


class ShapGlobalItem(BaseModel):
    feature: str
    importance: float


class ShapGlobalResponse(BaseModel):
    items: list[ShapGlobalItem]


class ShapLocalItem(BaseModel):
    feature: str
    contribution: float


class ShapLocalResponse(BaseModel):
    predicted_crop: str
    items: list[ShapLocalItem]
