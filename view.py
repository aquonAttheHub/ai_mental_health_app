from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

messages = [ {'role':'system', 'content':"""
   You are  a friendly assistant to assists with people's mental health needs. \
   You will keep waiting until the customer does not seek any help.
   You first greet the customer, then ask how they are doing. \


   If they are not feeling bad, then compliment them and ask what you can do for them.
   If they are not feeling well, then then ask what their issue is.


   If they have an issue, categorize their issue into one of the following categories:


   -Addiction
   -ADHD
   -Anger Management
   -Anxiety
   -Bipolar Disorder
   -Borderline Personality (BPD)
   -Depression
   -Eating Disorders
   -Grief
   -Marriage Counseling
   -Obsessive Compulsive (OCD)

   Once you have the category identified, ask if the customer is looking to find clinics that specialize in
   the issue they're facing. If yes, say that you will find the clinics shortly. If no, ask if there is anything else
   you can help with.


    """} ]


#Helper function to help modulate code.
def get_completion(messages, model="gpt-3.5-turbo", temperature=0, max_tokens = 500):
    #messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]



@app.route('/')
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    #Get the message input from the user
    user_input = request.form["message"]
    #Use the OpenAI API to generate a response
    
    #update messages with the user input
    messages.append({'role':'user', 'content':user_input})

    #Extract the response text from the OpenAPI result
    bot_response = get_completion(messages, model="gpt-3.5-turbo", temperature=0, max_tokens = 500)
    
    #update messages with the model response
    messages.append({'role': 'assistant', 'content': bot_response})
    return render_template("chatbot.html", user_input=user_input, bot_response=bot_response)


if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
