from openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv()

OLLAMA_API_KEY = 'ollama'
LLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = 'http://localhost:11434/v1'

def get_openai_client():
    return OpenAI(api_key=OLLAMA_API_KEY, base_url=OLLAMA_BASE_URL)

def get_llama_model():
    return LLAMA_MODEL
