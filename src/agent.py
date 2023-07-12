import openai
import os
import webscrape

MAX_DEPTH = 2
MAX_SUBTASKS = 3
openai.api_key = os.environ.get("OPENAI_API_KEY")

def user_answer(message: str)->list[str]:
    x = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"user", "content":f'Can this be answered the original prompter given their current knowledge: "{message}"Only respond with yes or no.'}]
    ).choices[0].message.content
    x=x.lower()
    if(x[0] == 'y'):
        return True
    return False

def parse_tasks(message: str)->list[str]:
    message = message.split('\n')
    tasks = []
    for i in range(1, min(MAX_SUBTASKS,len(message)-1)):
        tasks.append(message[i])
    return tasks

def summary(message: str)->str:
    return openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"user", "content":f"Summarize this. Make sure to keep key metrics and be specific: {message}"}]
    ).choices[0].message.content

class Agent:
    def __init__(self, prompt: str, depth: int):
        self.prompt = prompt
        self.depth = depth
    
    def for_user(self) -> bool:
        return False
    
    def is_leaf(self) -> bool:
        # ASK GPT IF THIS SOLVABLE W/ GOOGLE [?]
        return self.depth == MAX_DEPTH
    
    def generate_subtasks(self) -> list[str]:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": f'Create a list of topics to research to answer: "{self.prompt}". Make sure to make some of these easily answerable by the original prompter.'}]
        )
        tasks = result.choices[0].message.content
        return parse_tasks(tasks)
    
    def merge_queries(self, responses: list[str]) -> str:
        context = 'Process this information'
        for response in responses:
            context += response + '\n'
        context = context + f'Use the above answer to answer: "{self.prompt}" Make sure to use metrics to back you answer.'
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": context}]
        )
        return result.choices[0].message.content

    def run(self) -> str:
        print(f'Running task with depth {self.depth}...')
        if self.is_leaf():
            if user_answer(self.prompt):
                x = input(f"USER REQUEST: {self.prompt}\n")
                return x

            key_words = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user", "content": f'List 5 keywords to Google search for information about: {self.prompt}'}]
            ).choices[0].message.content
            articles = webscrape.urls.google_custom_search(key_words, 3)
            urls = [result["link"] for result in articles]
            data = webscrape.scrapedURLs.scrape_urls(urls)
            context = ""
            for i in range(len(data)):
                if data[i]["text"] != None:
                    context += summary(data[i]["text"][0:min(len(data[i]["text"]), 4096)]) + '\n';
            
            result = summary(context)
            return result
        else:
            subtasks = self.generate_subtasks()
            responses = []
            for task in subtasks:
                responses.append(Agent(f"This was the original Prompt: '{self.prompt}' \n Solve this subtask:" + task, self.depth+1).run())
            return self.merge_queries(responses)

    
if __name__ == '__main__':
    prompt = "My company is looking into entering electronics manufacturing. We currently produce $2 billion in revenue a year from our plastics production. However, we are not sure what the competition looks like and whether or not we should enter. We are very knowledgable about our finances and expertise. Should we enter this market?"
    test = Agent(prompt, 0)
    print(test.run())