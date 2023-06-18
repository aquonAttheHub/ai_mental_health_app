from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

messages = [ {'role':'system', 'content':"""
    You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collects the order, \
    and then asks if it's a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    If it's a delivery, you ask for an address. \
    Finally you collect the payment.\
    Make sure to clarify all options, extras and sizes to uniquely \
    identify the item from the menu.\
    You respond in a short, very conversational friendly style. \
    The menu includes \
    pepperoni pizza  12.95, 10.00, 7.00 \
    cheese pizza   10.95, 9.25, 6.50 \
    eggplant pizza   11.95, 9.75, 6.75 \
    fries 4.50, 3.50 \
    greek salad 7.25 \
    Toppings: \
    extra cheese 2.00, \
    mushrooms 1.50 \
    sausage 3.00 \
    canadian bacon 3.50 \
    AI sauce 1.50 \
    peppers 1.00 \
    Drinks: \
    coke 3.00, 2.00, 1.00 \
    sprite 3.00, 2.00, 1.00 \
    bottled water 5.00 \
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
