from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
import sys
try:
  openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
  sys.stderr.write("""
  You haven't set up your API key yet.
  
  If you don't have an API key yet, visit:
  
  https://platform.openai.com/signup

  1. Make an account or sign in
  2. Click "View API Keys" from the top right menu.
  3. Click "Create new secret key"

  Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
  """)
  exit(1)

# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )

# print(response)
app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
messages=[
      {"role": "system", "content": """You are OrderBot, an automated service to collect orders for a pizza restaurant. \
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
bottled water 5.00 """},
   ]
@app.route('/')
def index():
  # response = openai.ChatCompletion.create(
  # model="gpt-3.5-turbo",
  # messages=[
  #     {"role": "system", "content": "You are a helpful assistant."},
  #     {"role": "user", "content": "Who won the world series in 2020?"},
  #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
  #     {"role": "user", "content": "Where was it played?"}
  #  ]
  # )
  # print(response)
  # return(response.choices[0].message["content"])
  return "Welcome to devdasz api powered by chatGPT"


@app.route('/infer-review', methods=['POST'])
def getSummaryFromReview():
  # messages=[
  #     {"role": "system", "content": "You are a helpful assistant."},
  #  ]
  response = jsonify(role="assistant", content='Why did the chicken cross the road')
  # Enable Access-Control-Allow-Origin
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response
  # return {'role': 'assistant', 'content': 'Why did the chicken cross the road'}





@app.route('/chatbot', methods=['POST'])
def getChatReply():
  
  
  messages.append(request.json);
  # print(messages)
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages
  )
  print(response)
 


  content = response.choices[0].message["content"]
  response = jsonify(role="assistant",
                     content= content)
  messages.append({'role':'assistant', 'content':content});
  print(messages);
  # Enable Access-Control-Allow-Origin
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response
  # return {'role': 'assistant', 'content': 'Why did the chicken cross the road'}

@app.route('/post_json', methods=['POST'])

def process_json():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    json = request.json
    return json
  else:
    return 'Content-Type not supported!'


app.run(host='0.0.0.0', port=81)
