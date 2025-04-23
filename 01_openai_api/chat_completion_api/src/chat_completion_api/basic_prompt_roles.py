from openai import OpenAI
import os   
from dotenv import load_dotenv
 
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

# prompts = [
#     # Both are working for now and might me keep working in the future, but OpenAI's intenstion is clear
#     # they want to use developer role
#     { "role": "system", "content": "You are a javascipt developer"},
#     #{ "role": "developer", "content": "You are a javascipt developer"},
#     { "role": "user", "content": "javascript code to add two numbers"},
# ]


# response = openai.chat.completions.create(
#     model=MODEL,
#     #model=MISTRAL_MODEL,
#     messages= prompts
# )
# print(response.choices[0].finish_reason)
# print(response.choices[0].message.role)
# print(response.choices[0].message.content)

# responses api

prompts = [
    # { "role": "system", "content": "You are an helpfull assistant"},
    { "role": "developer", "content": "You are an helpfull assistant"},
    { "role": "user", "content": "do you remember the last conversations?"},
]

response = openai.responses.create(
    model=OPENAI_MODEL,
    input=prompts  # input property can accept both string as well as array of messages
)
print(response.output_text)
print(response)

print(response.instructions)
print(response.tools)
print(response.status)
print(response.store)