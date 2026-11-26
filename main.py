
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictionRequest
from .model import get_model, feature_importance

app=FastAPI(title="EstateIQ API",description="Educational demo; synthetic data by default.",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_methods=["*"],allow_headers=["*"])

@app.on_event("startup")
def startup(): get_model()

@app.get("/health")
def health(): return {"status":"ok","service":"EstateIQ API"}

@app.get("/metrics")
def metrics(): return get_model()[1]

@app.post("/predict")
def predict(x:PredictionRequest):
    model,_=get_model()
    row={"area_sqft":x.area_sqft,"bedrooms":x.bedrooms,"bathrooms":x.bathrooms,"property_age":x.property_age,
         "parking":int(x.parking),"furnished":int(x.furnished),"location":x.location}
    price=max(0,float(model.predict([row])[0])); rounded=round(price/100000)*100000
    return {"predicted_price_inr":round(price,2),"formatted_price":f"₹{rounded:,.0f}","location":x.location,
            "note":"Synthetic-data demo estimate only; not a real market valuation.","key_factors":feature_importance()}
