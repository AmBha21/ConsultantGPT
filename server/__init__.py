# import sys
from flask import Flask, request, jsonify
from src.agent import Agent
# sys.path.append('src/webscrape', 'src/agent')

app = Flask(__name__)

@app.route("/response")
def get_response():
    prompt = request.args.get('prompt')
    
    if __name__ == "__main__":
      agent = Agent(prompt, 0)
      return jsonify(agent.run())
    else:
      return "This function can only be run in the main thread."
  
if __name__ == "__main__":
  app.run()