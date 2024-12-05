from fastapi import FastAPI, APIRouter
from image_generator import GenerateImage
import json
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

class InputImage(BaseModel):
    input_data: str

@app.post('/image/')
def generate_image(input_image: InputImage):
    print(input_image)
    image = GenerateImage(input_image.input_data)
    image.embedding_text_prompt()
    image.generate_image()
    return {
        "status_code": 200,
        "body": "Image generated successfully!."
        }
app.include_router(router)