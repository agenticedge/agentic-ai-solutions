from config import get_openai_client, get_llama_model

def main():
    openai = get_openai_client()
    model = get_llama_model()
    # print(f"Using model: {model}")

    response = openai.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "give me a meal plan for a week and format it as a json object"},
        ]
    )

    print(f"Response: {response}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
