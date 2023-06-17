from flask import Flask, render_template
import os
import openai

app = Flask(__name__)



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]


@app.route('/')
def home():

    openai.api_key = os.getenv("OPENAI_API_KEY")

    return get_completion("What is 1+1?")

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
