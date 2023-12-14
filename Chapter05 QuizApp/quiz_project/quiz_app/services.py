from openai import OpenAI
import os
# API Token
client = OpenAI(
    # Retrieve the API key from the environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
)

def generate_questions(text):
    # Define your prompt for generating questions
    prompt = (
        f"Create a practice test with multiple choice questions "
        f"on the following text:\n{text}\n\n"
        f"Each question should be on a different line. Each "
        f"question should have 4 possible answers. "
        f"Under the possible answers, we should have the correct answer."
    )

    # Generate questions using the ChatGPT API
    response = client.completions.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=3500,
        stop=None,
        temperature=0.7
    )
    # Extract the generated questions from the API response
    questions = response.choices[0].text
    return questions