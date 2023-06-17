from flask import Flask, render_template
import os
import openai

app = Flask(__name__)

@app.route('/')
def home():

    openai.api_key = os.getenv("OPENAI_API_KEY")


    return render_template('index.html')

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
