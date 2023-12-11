#!/usr/bin/env python3
from flask import Flask, request, render_template
from openai import OpenAI
import os
import hashlib
import sqlite3
import stripe
import config

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

client = OpenAI(
    # Retrieve the API key from the environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
)
stripe.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    initialize_database()
    fingerprint = get_fingerprint()
    usage_counter = get_usage_counter(fingerprint)
    if request.method == "POST":
        if usage_counter > config.FREE_LIMIT:
            return render_template("payment.html")

        # Code Errr
        code = request.form["code"]
        error = request.form["error"]
        prompt = (f"Explain the error in this code without fixing it:"
                  f"\n\n{code}\n\nError:\n\n{error}")
        model_engine = "text-davinci-003"
        explanation_completions = client.completions.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.2,
        )
        explanation = explanation_completions.choices[0].text
        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
            f" \n Respond only with the fixed code."
        )

        fixed_code_completions = client.completions.create(
            model=model_engine,
            prompt=fixed_code_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.2,
        )
        fixed_code = fixed_code_completions.choices[0].text
        usage_counter += 1
        print(usage_counter)
        update_usage_counter(fingerprint, usage_counter)
        return render_template("index.html", explanation=explanation, fixed_code=fixed_code)

    # For GET requests, return a default response (you can modify this as needed)
    return render_template("index.html", explanation="", fixed_code="")


def initialize_database():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (fingerprint text primary
        key, usage_counter int)''')
    conn.commit()
    conn.close()

def get_fingerprint():
    browser = request.user_agent.browser
    version = request.user_agent.version and float(
        request.user_agent.version.split(".")[0])
    platform = request.user_agent.platform
    string = f"{browser}:{version}:{platform}"
    fingerprint = hashlib.sha256(string.encode("utf-8")).hexdigest()
    print(fingerprint)
    return fingerprint

def get_usage_counter(fingerprint):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    result = c.execute('SELECT usage_counter FROM users WHERE fingerprint=?', [fingerprint]).fetchone()
    conn.close()
    if result is None:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (fingerprint, usage_counter) VALUES ' '(?, 0)', [fingerprint])
        conn.commit()
        conn.close()
        return 0
    else:
        return result[0]

def update_usage_counter(fingerprint, usage_counter):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('UPDATE users SET usage_counter=? WHERE fingerprint=?',
                [usage_counter, fingerprint])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run()
