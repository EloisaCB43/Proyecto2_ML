import joblib
from pathlib import Path

MODEL_PATH = Path("models/best_lgbm_pipeline.pkl")

model = joblib.load(MODEL_PATH)