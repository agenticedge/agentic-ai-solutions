from openai import OpenAI
import os   
from dotenv import load_dotenv
import time
import base64
 
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

response = openai.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        { "role": "user", "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://media.istockphoto.com/id/1459502685/photo/engineer-factory-industry-wearing-safety-uniform-work-and-checking-system-of-the-welding.jpg?s=612x612&w=0&k=20&c=DPobvn2sSXvIxCN54ki8BIXwEsn6rcCFh6vhkPrCcyM=",
                },
            },
        ]}
    ]
)

print(response.choices[0].message.content)
     