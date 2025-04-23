from openai import OpenAI
import os   
from dotenv import load_dotenv
import time
 
load_dotenv()
# Get API keys from environment variables
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MISTRAL_BASE_URL = os.environ.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
MISTRAL_MODEL="mistral-large-latest"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
#OPENAI_BASE_URL = os.environ.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
OPENAI_MODEL="gpt-4o-mini"

api_key = 'ollama'
MODEL = "deepseek-r1:1.5b"
# DeepSeeker API key and base URL
DEEPSEEKER_API_KEY = 'ollama'
DEEPSEEKER_BASE_URL = 'http://localhost:11434/v1'

#openai = OpenAI(api_key=DEEPSEEKER_API_KEY, base_url=DEEPSEEKER_BASE_URL)
#openai = OpenAI(api_key=MISTRAL_API_KEY, base_url=MISTRAL_BASE_URL)
openai = OpenAI(api_key=OPENAI_API_KEY)

response = openai.responses.create(
    model=OPENAI_MODEL,
    input="Tell me a math joke",
)
print("Response 1 id = ",response.id)
print("Response 1 = ",response.output_text)
print("--------------------")

# Sending previous response id
response = openai.responses.create(
    model=OPENAI_MODEL,
    previous_response_id=response.id,
    input="Explain it to me",
)
print("Response 2 id = ",response.id)
print("Response 2 = ", response.output_text)