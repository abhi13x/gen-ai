from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from datetime import datetime
import os
from logger import logger
from validator.chat_message import ChatMessage
from validator.response_filter import ResponseFilter
from create_prompt import PromptEngineering

# Initialize Logger
logger = logger(__name__)

# Load environment variables
load_dotenv('.env')

# Initialize FastAPI app
app = FastAPI()
router = APIRouter()

# Add CORS middleware with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize HuggingFace Client
client = InferenceClient(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    api_key=os.getenv('HF_TOKEN')
)

async def log_request(message: str):
    logger.info(f"Request revceived at {datetime.now()}: {message[:100]}...")

@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        # Log the request
        await log_request(chat_message.message)

        # Create safe prompt with guardrails
        messages = PromptEngineering.create_safe_prompt(
            chat_message.message,
            chat_message.context
        )

        # Get completion from the model
        completion = client.chat.completions.create(
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )

        # Extract and filter the response
        raw_response = completion.choices[0].message.content.strip()
        print("XX"*10, raw_response)
        filtered_response = ResponseFilter.filter_output(raw_response)

        # Log the response
        logger.info(f"Response generated successfully for request.")

        return {
            "response": filtered_response,
            "filtered": filtered_response != raw_response
        }
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred. Please try again later., {str(e)}"
        )

if __name__ == "__main__":
   app.include_router(router)