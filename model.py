
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demo_house_prices.csv"
MODEL = Path(__file__).resolve().parent / "model.joblib"
NUM = ["area_sqft", "bedrooms", "bathrooms", "property_age", "parking", "furnished"]
CAT = ["location"]
LOC_RATE = {"Gurugram":8500,"Delhi":9000,"Noida":6500,"Sonipat":3800,"Jaipur":4200,"Bengaluru":7800}

def create_demo_data(n=1800, seed=42):
    rng=np.random.default_rng(seed); loc=rng.choice(list(LOC_RATE),n)
    area=rng.integers(450,3500,n)
    beds=np.clip(np.rint(area/550+rng.normal(0,.65,n)),1,6).astype(int)
    baths=np.clip(beds+rng.integers(-1,2,n),1,6).astype(int)
    age=rng.integers(0,35,n); parking=rng.integers(0,2,n); furnished=rng.integers(0,2,n)
    rate=np.array([LOC_RATE[x] for x in loc])
    price=area*rate*(1-age*.006)*(1+parking*.035+furnished*.025)*rng.normal(1,.12,n)
    df=pd.DataFrame({"area_sqft":area,"bedrooms":beds,"bathrooms":baths,"property_age":age,
      "location":loc,"parking":parking,"furnished":furnished,"price_inr":np.maximum(price,500000).round(0)})
    DATA.parent.mkdir(parents=True,exist_ok=True); df.to_csv(DATA,index=False); return df

def train():
    df=pd.read_csv(DATA) if DATA.exists() else create_demo_data()
    X=df[NUM+CAT]; y=df.price_inr
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
    prep=ColumnTransformer([("num",StandardScaler(),NUM),("cat",OneHotEncoder(handle_unknown="ignore"),CAT)])
    pipe=Pipeline([("prep",prep),("model",RandomForestRegressor(n_estimators=180,max_depth=16,min_samples_leaf=2,random_state=42,n_jobs=-1))])
    pipe.fit(Xtr,ytr); pred=pipe.predict(Xte)
    metrics={"mae_inr":float(mean_absolute_error(yte,pred)),"rmse_inr":float(np.sqrt(mean_squared_error(yte,pred))),
             "r2":float(r2_score(yte,pred)),"train_rows":len(Xtr),"test_rows":len(Xte),"dataset_type":"synthetic_demo"}
    joblib.dump({"pipe":pipe,"metrics":metrics},MODEL); return pipe,metrics

def get_model():
    if not MODEL.exists(): return train()
    obj=joblib.load(MODEL); return obj["pipe"],obj["metrics"]

def feature_importance():
    pipe,_=get_model(); model=pipe.named_steps["model"]
    catnames=pipe.named_steps["prep"].named_transformers_["cat"].get_feature_names_out(CAT)
    names=NUM+list(catnames)
    return [{"feature":str(k),"importance":round(float(v),4)} for k,v in sorted(zip(names,model.feature_importances_),key=lambda x:x[1],reverse=True)[:5]]
