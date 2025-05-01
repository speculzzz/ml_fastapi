from pydantic import BaseModel, Field


class FeaturesInput(BaseModel):
    """Scheme for input data."""
    sepal_length: float = Field(..., ge=0)
    sepal_width: float = Field(..., ge=0)
    petal_length: float = Field(..., ge=0)
    petal_width: float = Field(..., ge=0)


class PredictionOutput(BaseModel):
    """Scheme for a prediction."""
    class_id: int
    class_name: str
