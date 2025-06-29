from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from fastapi_keycloak import FastAPIKeycloak, OIDCUser

from app.models import model
from app.schemas import FeaturesInput, PredictionOutput, UserLogin


app = FastAPI(
    title="ML Model API",
    description="API for ML inference",
    version="0.1.0",
)
idp = FastAPIKeycloak(
    server_url="http://localhost:8080/",
    client_id="ml-fastapi",
    client_secret="i1yatCa3PX6PHx0MNp4rfng1HHHEfojb",
    admin_client_id="admin-fastapi",
    admin_client_secret="BCYObiw76A5CmdcE0MvEZVOFKXFeXkbk",
    realm="test-realm",
    callback_uri="http://localhost:8000/callback",
    ssl_verification=False,
)
idp.add_swagger_config(app)

IRIS_CLASS_NAMES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica",
}


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI ML Model Service"}


@app.post("/login")
async def login(user_data: UserLogin):
    """Get a GWT-token by creds"""
    try:
        # Get user's token
        token = idp.user_login(
            username=user_data.username,
            password=user_data.password
        )
        return {
            "access_token": token.access_token,
            "refresh_token": token.refresh_token,
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Authentification failed: {str(e)}"
        )


@app.get("/admin")
async def admin_route(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    """Only accessible by admins"""
    return {"message": "Admin access granted", "user": user}


@app.post("/predict", response_model=PredictionOutput)
async def predict(
        features: FeaturesInput,
        user: OIDCUser = Depends(idp.get_current_user(required_roles=["user"]))
):
    """Iris prediction ('user' authentification is required)"""
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


@app.get("/flexible")
async def flexible_route(user: OIDCUser = Depends(idp.get_current_user())):
    """Accessible for admins and users"""
    if "admin" not in user.roles and "user" not in user.roles:
        raise HTTPException(status_code=403, detail="Access denied")
    return {"message": "Access granted"}


@app.get("/callback", tags=["auth-flow"])
def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)
