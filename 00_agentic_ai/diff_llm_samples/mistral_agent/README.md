# Mistral Agent

Mistral Agent is a Python-based project that integrates with the Mistral API to create an AI-powered assistant. It leverages OpenAI's agent framework to run and interact with language models.

## Features

- Connects to the Mistral API using environment variables for secure authentication.
- Utilizes OpenAI's `AsyncOpenAI` and `OpenAIChatCompletionsModel` for model interactions.
- Provides a simple interface to run an AI agent with predefined instructions.

## Requirements

- Python 3.11 or higher
- Dependencies listed in `pyproject.toml`:
  - `ollama>=0.4.8`
  - `openai-agents>=0.0.12`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mistral_agent