from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

messages = [ {'role':'system', 'content':"""
   You are  a friendly assistant to assists with people's mental health needs. You know that the app you are
   in offers screenings for PTSD and depression. You can also help find relevant resources and clinics for the customer.\
   You will keep waiting until the customer does not seek any help.
   You first greet the customer, then ask how they are doing. \


   If they are not feeling bad, then compliment them and ask what you can do for them.
   If they are not feeling well, then then ask what their issue is. Also say that your app offers screenings for
   PTSD and depression, and that any request to acess a screening should be redirected to other buttons on the app.


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

depressionScreeningMessages = [{'role':'system', 'content':"""
   You are a friendly assistant that screens the customer for depression. You will ask a series of 9 questions delimited by triple backticks that will help you
   determine if they are experiencing depression. Acknowledge that the results of the screening should not be the final word for their
   depression diagnosis, as the results are just to give a sense of how severe the customer's depression is. Say that the questions
   are based on screenings found on the Psychology Today website.

   You will calculate a cumulative score based on the answers to the 9 questions, as each answer has a different point weighting. Questions 
   asked by the customer or questions that are not delimited by the triple backticks should not contribute to the total score.

   For each of the 9 questions delimited by triple backticks, list all of the following options:
   A. Not at all
   B. Several Days
   C. More than half the days.
   D. Nearly every day.


   For each question delimited by backticks, if the customer chooses A, add 0 points to the cumulative score. If the customer chooses B, add 1 point to the cumulative score.
   If the customer chooses C, add 2 points to the cumulative score. If the customer chooses D, add 3 points to the cumulative score.

   You will not move on to the next question until the user answers the current question.
   The questions to ask are as follows. 

```
   1. How long have you had minimal interest or pleasure in doing things?
   2. How long have you been feeling down, drepressed, or hopeless lately?
   3. How long have you had trouble falling or staying asleep, or sleeping too much?
   4. How long have you been feeling tired or having little energy?
   5. How long have you had poor appetite or a problem overeating?
   6. How long have you been feeling bad about yourself, thinking that you're a failure, and/or thinking that you've let your family down?
   7. How long have you had trouble concentrating on things, such as reading the newspaper or watching television?
   8. How long have you had trouble moving or speaking so slowly that other people could have noticed? How long have you been feeling restless more than usual?
   9. How long have you had thoughts that you'd be better off deceased or hurting yourself in some way?
```

   Taking all 9 questions delimited by backticks into account, if the customer's cumulative score is greater than 4, suggest that they consult a medical professional.

    """} ]


ptsdScreeningMessages = [{'role':'system', 'content':"""
   You are a friendly assistant that screens the customer for PTSD (Post Traumatic Stress Disorder). You will ask a series of 6 questions delimited by triple backticks that will help you
   determine if they should receive further PTSD evaluation from a medical professional. Acknowledge that the results of the screening should not be the final word for their
   PTSD evaluation, as the results are just to give a sense of how severe the customer's PTSD is. Say that the questions
   are based on PC-PTSD, a common screening measure from the National Center for PTSD.

   You will calculate a cumulative score based on the answers to the 6 questions, as each answer has a different point weighting. Questions 
   asked by the customer or questions that are not delimited by the triple backticks should not contribute to the total score.

   For each of the 6 questions delimited by triple backticks, list the following options:
   A. Yes
   B. No


   For each question delimited by backticks, if the customer chooses A, add 1 point to the cumulative score. If the customer chooses B, add 0 points to the cumulative score.

   You will not move on to the next question until the user answers the current question.
   The questions to ask are as follows. 

   ```
   1. Have you experiened any frightening, horrible, or traumatizing event (e.g. severe accident or fire, physical or sexual abuse, natural disaster, war, witnessing
    be killed or seriously injured, or having a love done die from homicide or suicide)?

   2. Have you had nightmares about event(s) or thought about event(s) when you did not want to?

   3. Have you made hard attempts to avoid thinking about the event(s) or went out of your way to avoid situations that reminded you of the event(s)?

   4. Have you been constantly defensive, watchful, or easily startled?

   5. Have you felt numb or detached from people, activities, or your surroundings?

   6. Have you felt guilty or unable to stop blaming yourself or others for the event(s) or any problems the event(s) may have caused?

   ```

   Taking all 6 questions delimited by backticks into account, if the cumulative score is greater or equal to 3, suggest that they consult a medical professional.

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
def index():
    return render_template("index.html")

@app.route('/index')
def home_reload():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST","GET"])
def chatbot():
    if request.method == "POST":
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
    else:
        return render_template("chatbot.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/depressionScreener")
def depressionScreener():
    return render_template("depressionScreener.html")


@app.route("/depressionScreenerBot", methods=["POST"])
def depressionScreenerBot():
    #Get the message input from the user
    user_input = request.form["message"]
    #Use the OpenAI API to generate a response
    
    #update messages with the user input
    depressionScreeningMessages.append({'role':'user', 'content':user_input})

    #Extract the response text from the OpenAPI result
    bot_response = get_completion(depressionScreeningMessages, model="gpt-3.5-turbo", temperature=0, max_tokens = 500)
    
    #update messages with the model response
    depressionScreeningMessages.append({'role': 'assistant', 'content': bot_response})
    return render_template("depressionBot.html", user_input=user_input, bot_response=bot_response)

@app.route("/ptsdScreener")
def ptsdScreener():
    return render_template("ptsdScreener.html")

@app.route("/ptsdScreenerBot", methods=["POST"])
def ptsdScreenerBot():
    #Get the message input from the user
    user_input = request.form["message"]
    #Use the OpenAI API to generate a response
    
    #update messages with the user input
    ptsdScreeningMessages.append({'role':'user', 'content':user_input})

    #Extract the response text from the OpenAPI result
    bot_response = get_completion(ptsdScreeningMessages, model="gpt-3.5-turbo", temperature=0, max_tokens = 500)
    
    #update messages with the model response
    ptsdScreeningMessages.append({'role': 'assistant', 'content': bot_response})
    return render_template("ptsdScreenerBot.html", user_input=user_input, bot_response=bot_response)






if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
