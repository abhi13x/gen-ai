from ollama import Client
from langchain_ollama.chat_models import ChatOllama

# Initialize the LLM (Using a placeholder for OpenAI/Google LLM)
# NOTE: Replace with your actual LLM and API key setup
async def model_init(api_key: str, llm_model: str, llm_temperature: float):
    try:
        Client(
            host="https://ollama.com",
            headers={
                'Authorization': f"Bearer {api_key}"
                })
        llm = ChatOllama(
            temperature=llm_temperature,
            model=llm_model
            )
        print(f"LLM Model '{llm_model}' initialized with temperature {llm_temperature}")
        return llm
    except Exception as e:
        print(f"LLM Initialization error LLM Model '{llm_model}' with temperature {llm_temperature}: {e}")
        raise RuntimeError(e)