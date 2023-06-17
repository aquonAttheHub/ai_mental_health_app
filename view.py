from flask import Flask, render_template
import os
import openai

app = Flask(__name__)



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

    openai.api_key = os.getenv("OPENAI_API_KEY")

    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries.
    The customer service query will be delimited with 
    {delimiter} characters.
    Classify each query into a primary category
    and a secondary category. 
    Provide your output in json format with the
    keys: primary and secondary.

    Primary categories: Billing, Technical Support,
    Account Management, or General Inquiry.

    Billing secondary categories:
    Unsubscribe or upgrade
    Add a payment method
    Explanation for charge
    Dispute a charge

    Technical Support secondary categories:
    General troubleshooting
    Device compatibility
    Software updates

    Account Management secondary categories:
    Password reset
    Update personal information
    Close account
    Account security

    General Inquiry secondary categories:
    Product information
    Pricing
    Feedback
    Speak to a human

    """
    user_message = f"""I want you to delete my profile and all of my user data"""
    messages =  [  
    {'role':'system', 
    'content': system_message},    
    {'role':'user', 
    'content': f"{delimiter}{user_message}{delimiter}"},  
    ]
    
    response = get_completion(messages)
    print(messages)
    return response

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
