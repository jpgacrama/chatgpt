from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = "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",
)

question = input("What would you like to ask ChatGPT? ")
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content": question}],
    engine="text-davinci-003",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.8,
)

print(response)