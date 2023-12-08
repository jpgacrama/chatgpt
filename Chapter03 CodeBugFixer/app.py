#!/usr/bin/env python3
from flask import Flask, request, render_template
from openai import OpenAI
import os

def clear_screen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

client = OpenAI(
    # Retrieve the API key from the environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
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
        return render_template("index.html", explanation=explanation, fixed_code=fixed_code)

    # For GET requests, return a default response (you can modify this as needed)
    return render_template("index.html", explanation="", fixed_code="")

if __name__ == "__main__":
    app.run()
