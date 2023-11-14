from openai import OpenAI
import os
import config

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

client = OpenAI(
    api_key = config.API_KEY,
)

question = input("What would you like to ask ChatGPT? ")
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content": question}],
    max_tokens = 1024,
    n = 1,
    stop = None,
    temperature = 0.8,
)
