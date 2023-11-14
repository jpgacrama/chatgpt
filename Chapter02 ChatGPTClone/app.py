#!/usr/bin/env python3

from flask import Flask
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
    return "Hello, World!"
if __name__ == "__main__":
    app.run()