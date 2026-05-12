from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd

from app.predictor import model

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    area: float = Form(...),
    estrato: int = Form(...),
    banos: int = Form(...),
    habitaciones: int = Form(...),
    parqueaderos: int = Form(...),
    tipo_inmueble: str = Form(...),
    estado: str = Form(...),
    antiguedad: str = Form(...),
    barrio_group: str = Form(...),
    piso_cat: str = Form(...),
):
    
    data = pd.DataFrame(
        [{
            "Área Construida (m2)": area,
            "Estrato": estrato,
            "Baños": banos,
            "Habitaciones": habitaciones,
            "Parqueaderos": parqueaderos,
            "Tipo de Inmueble": tipo_inmueble,
            "Estado": estado,
            "Antigüedad": antiguedad,
            "Barrio_group": barrio_group,
            "Piso_cat": piso_cat,
        }]
    )

    prediction = model.predict(data)[0]

    prediction = f"${prediction:,.0f} COP"

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "prediction": prediction,
    },
)

##uvicorn app.main:app --reload
##http://127.0.0.1:8000