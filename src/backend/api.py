from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, BeforeValidator
from typing import Annotated

from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import joblib
import pandas as pd


def valid_material(value: str) -> str:
    """validate  material must be N,P or K"""
    material = ["N", "P", "K"]
    if (value not in material):
        raise ValueError("Material must be N,P or K")
    return value


def valid_drill_bit(value: str) -> str:
    """validate drill bit must W,N or H"""
    drill_bit_type = ["W", "N", "H"]
    if (value not in drill_bit_type):
        raise ValueError("Drill bit must be must be W,N or H")
    return value


def valid_cooling(value: int) -> int:
    """validate cooling"""
    cooling_values = [0, 25, 50, 75, 100]
    if (value not in cooling_values):
        raise ValueError("Cooling must be 0,25,50,75, or 100")
    return value


def validate_cutting_speed(value: float):
    if ((value >= 16) and (value <= 35)):
        return value
    raise ValueError("Cutting speed must be between 16 and 35")


def validate_spindle_speed(value: int):
    if ((value >= 400) and (value <= 830)):
        return value
    raise ValueError("Spindle speed must be between 400 and 830")


def validate_feed(value: float):
    if ((value >= .100) and (value <= .325)):
        return value
    raise ValueError("Feed value must be between .100 and .325")


def validate_feed_rate(value: int):
    if ((value >= 60) and (value <= 265)):
        return value
    raise ValueError("feed rate must be between 60 and 265")


def validate_power(value: float):
    if ((value >= 45) and (value <= 310)):
        return value
    raise ValueError("Power must be between 45 and 310")


def validate_process_time(value: float):
    if ((value >= 15) and (value <= 40)):
        return value
    raise ValueError("Process time must be between 15 and 40")


class DrillMetric(BaseModel):
    cutting_speed_vc: Annotated[float, BeforeValidator(validate_cutting_speed)]
    spindle_speed_n: Annotated[int, BeforeValidator(validate_spindle_speed)]
    feed_f: Annotated[float, BeforeValidator(validate_feed)]
    feed_rate_vf: Annotated[int, BeforeValidator(validate_feed_rate)]
    power_pc: Annotated[float, BeforeValidator(validate_power)]
    cooling: Annotated[int, BeforeValidator(valid_cooling)]
    material: Annotated[str, BeforeValidator(valid_material)]
    drill_bit_type: Annotated[str, BeforeValidator(valid_drill_bit)]
    process_time: Annotated[float, BeforeValidator(validate_process_time)]


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Override"""
    txt = []
    for err in exc.errors():

        field = err["loc"][0]

        if (len(err["loc"]) > 1):
            field = err["loc"][1]

        row = {"field": field, "msg": err["msg"]}
        txt.append(row)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(
            {"success": False, "errors": txt}),
    )

model = joblib.load("src/models/xai.joblib")

origins = [
    "http://0.0.0.0:8000/",
    "http://localhost:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


@app.get("/")
def home():
    """Function is home index"""
    return ("API running")


@app.post("/predict")
async def predict(data: DrillMetric):
    """Predict the result"""
    # print(data.drill_bit_type)
    sample = pd.DataFrame([{
        "cutting_speed_vc": data.cutting_speed_vc,
        "spindle_speed_n": data.spindle_speed_n,
        "feed_f": data.feed_f,
        "feed_rate_vf": data.feed_rate_vf,
        "power_pc": data.power_pc,
        "cooling": data.cooling,
        "material": data.material,
        "drill_bit_type": data.drill_bit_type,
        "process_time": data.process_time
    }])
    # print(sample)

    prediction = model.predict(sample)
    result = prediction[0]
    response = {
        "success": True,
        "result": [
            {
                "main_failure": int(result[0]),
                "buildup_edge_failure": int(result[1]),
                "compression_chip_failure": int(result[2]),
                "flank_wear_failure": int(result[3]),
                "wrong_drill_bit_failure": int(result[4]),
            }
        ]
    }

    return JSONResponse(content=jsonable_encoder(response))
