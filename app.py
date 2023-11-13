from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = "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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

question = input("What would you like to ask ChatGPT? ")
response = client.chat.completions.create(
    engine="text-davinci-003",
    prompt=question,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.8,
)

print(response)