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


prompts = [
    { "role": "user", "content": "Tell me a joke about the internet"}
]
stream = openai.responses.create(
    model=OPENAI_MODEL,
    input=prompts,  # input property can accept both string as well as array of messages
    stream=True,  # Uncomment this line to enable streaming
)

message = ""

# Process the streaming response
for event in stream:
    if hasattr(event, "delta") and event.delta:  # Check if the event has a delta attribute
        message += event.delta
        print(event.delta, end="", flush=True)  # Print the delta incrementally
        time.sleep(0.2)  # Add a delay for better readability

print("\nFinal Message:", message)