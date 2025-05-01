from fastapi import FastAPI
from fastapi.responses import Response

from app.models import model
from app.schemas import FeaturesInput, PredictionOutput


app = FastAPI(
    title="ML Model API",
    description="API for ML inference",
    version="0.1.0",
)

IRIS_CLASS_NAMES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica",
}


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI ML Model Service"}


@app.post("/predict", response_model=PredictionOutput)
async def predict(features: FeaturesInput):
    """Iris prediction."""
    input_features = [
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]

    class_id = model.predict(input_features)

    return {
        "class_id": class_id,
        "class_name": IRIS_CLASS_NAMES.get(class_id, "unknown"),
    }


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)
