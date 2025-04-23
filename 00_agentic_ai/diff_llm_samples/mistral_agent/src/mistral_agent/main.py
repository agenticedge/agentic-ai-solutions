import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

def run_agent() -> None:
    print("Hello from mistral-agent!")
    # Load the environment variables from the .env file
    load_dotenv()
    # Get API keys from environment variables
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    MISTRAL_BASE_URL = os.environ.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")

    # DeepSeeker API key and base URL
    DEEPSEEKER_API_KEY = 'ollama'
    DEEPSEEKER_BASE_URL = 'http://localhost:11434/v1'

    # Check if the API key is present; if not, raise an error
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is not set. Please ensure it is defined in your .env file.")

    external_client = AsyncOpenAI(
        #api_key=MISTRAL_API_KEY,
        #base_url=MISTRAL_BASE_URL,
        api_key=DEEPSEEKER_API_KEY,
        base_url=DEEPSEEKER_BASE_URL,
    )

    model = OpenAIChatCompletionsModel(
        #model="mistral-large-latest",
        model="deepseek-r1:1.5b",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

    result = Runner.run_sync(agent, "which llm model you are using?", run_config=config)

    print("\nCALLING AGENT\n")
    print(result.final_output)