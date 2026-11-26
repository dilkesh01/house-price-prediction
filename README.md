# EstateIQ — House Price Prediction

Full-stack educational demo using React, FastAPI and scikit-learn.

## Features
- Predict a demo property price from area, bedrooms, bathrooms, age, location, parking and furnishing.
- Random Forest regression pipeline with preprocessing.
- MAE, RMSE and R² metrics.
- Global feature-importance guidance.
- Responsive dashboard and recent estimates.

> IMPORTANT: The included dataset is synthetic and only demonstrates the ML/software pipeline. Predictions are NOT real market valuations. Replace it with a properly licensed, representative dataset before making accuracy or market claims.

## Run

### Backend (Python 3.10+)
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000/docs

### Frontend (Node.js 18+)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## API
- `GET /health`
- `GET /metrics`
- `POST /predict`

Example request:
```json
{"area_sqft":1500,"bedrooms":3,"bathrooms":2,"property_age":5,"location":"Gurugram","parking":true,"furnished":false}
```

## Next improvements
Use real licensed data, add cross-validation/model comparison, SHAP local explanations, tests, PostgreSQL persistence, Docker and deployment.
