import openai
import os
import webscrape

MAX_DEPTH = 1
MAX_SUBTASKS = 3
openai.api_key = os.environ.get("OPENAI_API_KEY")

def parse_tasks(message: str)->list[str]:
    tasks = []
    for i in range(len(message)):
        #Double Digits!
        if message[i] == '.' and ord(message[i-1]) - ord('0') == len(tasks)+1:
            if len(tasks) > MAX_SUBTASKS:
                break
            tasks.append("")
        elif len(tasks) != 0:
            tasks[len(tasks)-1] += message[i]
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
            messages=[{"role":"user", "content": f'Create a list of topics to research to answer: {self.prompt}'}]
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
        print(f'Running task {self.prompt}...')
        if self.for_user():
            return input(f'User Request {self.prompt}')
        elif self.is_leaf():
            key_words = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user", "content": f'List 5 keywords from this prompt: {self.prompt}'}]
            ).choices[0].message.content
            articles = webscrape.urls.google_custom_search(key_words, 3)
            urls = [result["link"] for result in articles]
            data = webscrape.scrapedURLs.scrape_urls(urls)
            context = ""
            for i in range(len(data)):
                if data[i]["text"] != None:
                    context += summary(data[i]["text"][0:min(len(data[i]["text"]), 2000)]) + '\n';
            
            result = summary(context)
            return result
        else:
            subtasks = self.generate_subtasks()
            responses = []
            for task in subtasks:
                responses.append(Agent(task, self.depth+1).run())
            return self.merge_queries(responses)

    
if __name__ == '__main__':
    test = Agent("My company is looking into manufacturing electric vehicles. Currently we produce plastics and small electronics. We estimate a 30% profit margin per car sold. What business strategies should we run for production and advertising? Be concrete.", 0)
    print(test.run())