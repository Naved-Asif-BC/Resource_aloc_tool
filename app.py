from flask import Flask, render_template, request
import openai
import os 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

data={
    "people": [
        {
            "Name": "Naved",
            "Skills": ["Java", "Python", "SQL","Machine Learning","Deep Learning","GenAI","prompt engineering","Power Automate"],
            "Availability": "False"
        },
        {
            "Name": "Yash",
            "Skills": ["JavaScript", "CSS", "HTML","MongoDB","Angular"],
            "Availability": "False"
        },
        {
            "Name": "Ronak",
            "Skills": ["aws", "azure", "ETL","Data Engineering","AWS glue"],
            "Availability": "False"
        },
        {
            "Name": "Mohit",
            "Skills": ["Python", "SQL","Machine Learning","Deep Learning","GenAI","prompt engineering","Power virtual agent"],
            "Availability": "False"
        },
        {
            "Name": "Tanay",
            "Skills": ["Project Management","Communication","Requirements gathering","Strategy"],
            "Availability": "True"
        },
         {
            "Name": "Omkar",
            "Skills": ["Photoshop", "designing", "UI/UX","ETL","analytics","Azure"],
            "Availability": "True"
        },
         {
            "Name": "Abhishek",
            "Skills": ["Machine Learning", "Python", "Mongodb","Frontend","Backend","Data analysis"],
            "Availability": "True"
        },
         {
            "Name": "Sakshi",
            "Skills": ["Project MAnagement","Team Management","Jira","Product Management","Communication"],
            "Availability": "True"
        },
         {
            "Name": "Jahanwi",
            "Skills": ["Python","Machine Learning","Prompt Engineering"],
            "Availability": "True"
        }
    ]
}

# Initialize conversation list
conversation = [{'role':'system', 'content':f"""
You are a resource allocator.
Analyse the data given below
{data} 
and give TOP 3 people suitable for the requirement.

Requirement will be given by user.

Do Consider the availbility of the person, otherwise you will be penalised.

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
    app.run(debug=True,host="0.0.0.0")

