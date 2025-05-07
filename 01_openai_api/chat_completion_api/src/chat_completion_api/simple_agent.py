from agents import Agent, Runner
from dotenv import load_dotenv
import os
import asyncio
async def main():
    # Load environment variables from .env file
    load_dotenv()
    # Get API keys from environment variables
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["OPENAI_MODEL"] = OPENAI_MODEL

    agent = Agent(
        name="WeatherAgent",
        instructions="A helpful assistant that provides weather updates.",

    )

    response = await Runner.run(
        agent,
        "What is the weather in Karachi, Pakistan?",
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())