#!/usr/bin/env python3

from flask import Flask, render_template, request
from openai import OpenAI
import config
import os

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

client = OpenAI(
    api_key = config.API_KEY,
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    messages=[
        {"role": "user", "content": userText},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )
    answer=response.choices[0].message.content
    return str(answer)

if __name__ == "__main__":
    app.run()
