from openai import OpenAI
import os   
from dotenv import load_dotenv
 
load_dotenv()
# Get API keys from environment variables
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MISTRAL_BASE_URL = os.environ.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
MISTRAL_MODEL="mistral-large-latest"

api_key = 'ollama'
MODEL = "deepseek-r1:1.5b"
# DeepSeeker API key and base URL
DEEPSEEKER_API_KEY = 'ollama'
DEEPSEEKER_BASE_URL = 'http://localhost:11434/v1'

#openai = OpenAI(api_key=DEEPSEEKER_API_KEY, base_url=DEEPSEEKER_BASE_URL)
openai = OpenAI(api_key=MISTRAL_API_KEY, base_url=MISTRAL_BASE_URL)

prompts = [
    { "role": "user", "content": "how are you?"}
]

response = openai.chat.completions.create(
    model=MISTRAL_MODEL,
    messages= prompts
)


print(f'Response.choices[0]: {response.choices[0]}')
print()
print(f'Response.choices[0].message: {response.choices[0].finish_reason}')
print()
print(f'Response.choices[0].message: {response.choices[0].message}')
print(f'Response.choices[0].message.role: {response.choices[0].message.function_call}')
print(f'Response.choices[0].message.content: {response.choices[0].message.tool_calls}')
print(f'Response.choices[0].message.annotations: {response.choices[0].message.annotations}')
print()
print(f'Response.choices[0].message.content: {response.choices[0].message.content}')