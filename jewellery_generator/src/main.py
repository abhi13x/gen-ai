from fastapi import FastAPI, APIRouter
from image_generator import GenerateImage
import json

app = FastAPI()
router = APIRouter()

@app.get('/')
def generate_image(input_data: str):
    GenerateImage(input_data)
    return json.dump({
        "status_code": 200,
        "body": "Image generated successfully!."
        })
app.include_router(router)