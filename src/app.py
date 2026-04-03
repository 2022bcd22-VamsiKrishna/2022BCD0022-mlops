from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class HousingData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "Name": "Vamsi Krishna Vutla",
        "Roll_Number": "2022BCD0022",
        "Status": "API is Healthy and Running"
    }

@app.post("/predict")
def predict(data: HousingData):
    prediction = (data.MedInc * 0.4) + (data.HouseAge * 0.01) 
    
    return {
        "Name": "Vamsi Krishna Vutla",
        "Roll_Number": "2022BCD0022",
        "Predicted_House_Value": round(prediction, 2)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)