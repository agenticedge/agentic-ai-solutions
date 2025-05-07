import chainlit as cl
from openai import OpenAI
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

from agents.run import RunConfig
import os   
from dotenv import load_dotenv
import time
from tools import get_weather_function_chat
 
load_dotenv()
# Get API keys from environment variables
DEEPSEEKER_API_KEY = 'ollama'
DEEPSEEKER_BASE_URL = 'http://localhost:11434/v1'

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


@cl.on_message
async def main(message: cl.Message):
    # input = [
    #     { "role": "user", "content": message.content},
    # ]

    response = await Runner.run(agent, message.content, run_config=config)
    await cl.Message(
            content=response.final_output
        ).send()