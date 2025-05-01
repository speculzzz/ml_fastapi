import pytest
from pydantic import ValidationError
from app.schemas import FeaturesInput
from app.models import model


def test_features_input_validation():
    """Test validation of input features"""
    # Valid data
    valid_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    FeaturesInput(**valid_data)  # Should not raise an error

    # Invalid data (negative values)
    invalid_data = valid_data.copy()
    invalid_data["sepal_length"] = -1.0

    with pytest.raises(ValidationError) as exc_info:
        FeaturesInput(**invalid_data)

    errors = exc_info.value.errors()
    assert any(
        error["loc"] == ("sepal_length",)
        and error["type"] == "greater_than_equal"
        for error in errors
    )

@pytest.mark.parametrize(
    "features, expected_class",
    [
        ([5.1, 3.5, 1.4, 0.2], 0), # setosa
        ([5.9, 3.0, 4.2, 1.5], 1), # versicolor
        ([6.9, 3.1, 5.4, 2.1], 2)  # virginica
    ]
)
def test_model_prediction(features, expected_class):
    """Test model prediction accuracy"""
    assert model.predict(features) == expected_class

def test_borderline_case():
    """Borderline test case between versicolor and virginica"""
    borderline_features = [6.0, 3.0, 4.8, 1.8]

    # Check that the prediction belongs to one of two classes
    prediction = model.predict(borderline_features)
    assert prediction in [1, 2]

    # Checking the probabilities
    probas = model.predict_proba(borderline_features)
    assert abs(probas[1] - probas[2]) < 0.3  # The difference in probabilities is small

def test_predict_endpoint(client):
    """Test /predict API endpoint"""
    test_payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=test_payload)

    assert response.status_code == 200
    assert response.json() == {
        "class_id": 0,
        "class_name": "setosa"
    }

def test_invalid_input_handling(client):
    """Test API handling of invalid input"""
    response = client.post("/predict", json={"invalid": "data"})
    assert response.status_code == 422  # Unprocessable Entity

def test_response_structure(client):
    """Test response structure and data types"""
    test_payload = {
        "sepal_length": 6.3,
        "sepal_width": 2.8,
        "petal_length": 5.1,
        "petal_width": 1.5
    }
    response = client.post("/predict", json=test_payload)

    data = response.json()
    assert isinstance(data["class_id"], int)
    assert isinstance(data["class_name"], str)
    assert data["class_id"] in [0, 1, 2]
