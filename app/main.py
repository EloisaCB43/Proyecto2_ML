from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd

from app.predictor import model

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def default_form_data():
    return {
        "area": "",
        "estrato": 3,
        "banos": 1,
        "habitaciones": 1,
        "parqueaderos": 0,
        "tipo_inmueble": "",
        "estado": "",
        "antiguedad": "",
        "barrio_group": "",
        "piso_cat": 1,
    }


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"form_data": default_form_data()},
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
    form_data = {
        "area": area,
        "estrato": estrato,
        "banos": banos,
        "habitaciones": habitaciones,
        "parqueaderos": parqueaderos,
        "tipo_inmueble": tipo_inmueble,
        "estado": estado,
        "antiguedad": antiguedad,
        "barrio_group": barrio_group,
        "piso_cat": piso_cat,
    }

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
        "form_data": form_data,
    },
)

##uvicorn app.main:app --reload
##http://127.0.0.1:8000
