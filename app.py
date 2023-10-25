from flask import Flask, render_template, request
from dotenv import load_dotenv
from data import data  
import openai
import os 

load_dotenv()


app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]


# Initialize conversation list
conversation = [{'role':'system', 'content':f"""
You are a resource allocator.
Analyse the data given below

{data}
 
Strictly try to produce results from people whose "availablity" is marked as "True" otherwise you will be PENALISED.
STRICTLY give TOP 3 people suitable for the requirement.
Requirement will be given by user.
Always mention the availabilty of the people.
"""}]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    # Get user input from the form
    user_input = request.form['user_input']
    
    # Append user input to conversation
    conversation.append({'role':'user', 'content':f"{user_input}"})
    
    # Get response from OpenAI API
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        temperature=0.0,
        messages = conversation,
    )
    
    # Append OpenAI's response to conversation
    assistant_response = response.choices[0].message["content"]

    if len(conversation) == 10:
        conversation.pop(1)
        conversation.pop(2)
    conversation.append({'role':'assistant', 'content':f"{assistant_response}"})
    return {'response': assistant_response}

if __name__ == '__main__':
    app.run(debug=True,port=8080)

