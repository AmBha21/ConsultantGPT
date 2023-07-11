import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def ProcessInput(input, message_history):
  message_history.append({"role": "user", "content": input}) # append the user input
  
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_history
  ) # generate openai response
  
  message_history.append(completion.choices[0].message) # append openai response to the message history
      
  
def RecursiveInput(message_history):
  if not message_history[-1].content.startswith("input:"):
    return 
  
  prompt = message_history[-1].content
  new_input = input(prompt[7:]) # remove the "input:" from the prompt
  ProcessInput(new_input, message_history)
  RecursiveInput(message_history)
  

def GenerateSearchQueries(message_history):
  if not message_history[-1].content.startswith("search-queries:"):
    return 
  
  search_prompt = '''
    Now generate the second set of questions.
    This is going to be a list of search queries you would make to find the up-to-date information on the topic that would help you to better answer the question.
    The format of these questions you're going to respond with is "search-queries: [query1, query2, query3]".
    Some of your search questions should be for market data within the current field.
  '''

  # maybe should be a different role
  message_history.append({"role": "system", "content": search_prompt}) # append the search prompt
  
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_history
  ) # generate openai response
  
  message_history.append(completion.choices[0].message) # append openai response to the message history
  print('your search queries: ', message_history[-1].content[16:])

      
initial_prompt = '''
  You are a consultant designed to help manufacturing companies. 
  You are you going to ask two sets of questions to generate the information you need to properly answer the question.
  The first set of questions is going to be questions you have for the company to understand their situation.
  You are going to ask these in the format of "input: question?". 
  Only ask one question at a time.
  Only ask a limit of 5 questions for this first set of questions.
  Continusouly ask questions until you believe you have enough all the information you need from the client.
  Then you are going to generate the second set of questions. 
  This set of questions is going to be a list of search queries you would make to find the up-to-date information on the topic that would help you to better answer the question.
  The format of these questions you're going to respond with is "search-queries: [query1, query2, query3]".
'''

message_history = [
  {"role": "system", "content": initial_prompt},
]

user_input = '''
  I have a manufacturing company that is looking to get involved in producing electric vehicles. What are the steps I need to take to get involved in producing electric vehicles?
''' # testing purposes

ProcessInput(user_input, message_history)
RecursiveInput(message_history)
GenerateSearchQueries(message_history)
print('message history at the end: ', message_history)