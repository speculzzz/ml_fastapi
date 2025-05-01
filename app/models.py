from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class MLIrisModel:
    def __init__(self):
        # Use Iris dataset
        x, y = load_iris(return_X_y=True)
        x_train, _, y_train, _ = train_test_split(x, y, random_state=42)

        # Training the model
        self.model = LogisticRegression(random_state=42, max_iter=1000)  # To fix seed
        self.model.fit(x_train, y_train)

    def predict(self, features: list[float]) -> int:
        """Feature-based prediction."""
        return int(self.model.predict([features])[0])

    def predict_proba(self, features: list[float]) -> list[float]:
        """Class probabilities."""
        return self.model.predict_proba([features])[0]


# Initializing the model when the application starts
model = MLIrisModel()
