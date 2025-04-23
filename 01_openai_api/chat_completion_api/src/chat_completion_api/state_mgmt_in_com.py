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

# Using this array for adding all the messages in the conversation
history = [
    { "role": "user", "content": "Tell me a math joke"},
]

response = openai.chat.completions.create(
    model=OPENAI_MODEL,
    messages= history
)
print(response.choices[0].message.content)

history.append(response.choices[0].message) # Adding last response from Chat API to history
history.append({ "role": "user", "content": "Explain it to me"})
response2 = openai.chat.completions.create(
    model=OPENAI_MODEL,
    messages= history
)
print(response2.choices[0].message.content)