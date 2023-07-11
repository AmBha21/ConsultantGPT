import openai
import os

MAX_DEPTH = 5
MAX_SUBTASKS = 3
openai.api_key = os.environ.get("OPENAI_API_KEY")

def parse_tasks(message: str)->list[str]:
    return ["Example"]

class Agent:
    # Agent --> Is Leaf -TRUE--> Return Summary
    #                   -FALSE-> Generate List
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
        context = ''
        for response in responses:
            context += response + '\n'
        context = context + f'Use the above answer to answer: {self.prompt}'
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": context}]
        )
        return result.choices[0].message.content

    def run(self) -> str:
        if self.for_user():
            return input(f'User Request {self.prompt}')
        elif self.is_leaf():
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user", "content": f'Provide a summary on this topic: {self.prompt}'}]
            )
            return result.choices[0].message.content
        else:
            subtasks = self.generate_subtasks()
            responses = []
            for task in subtasks:
                responses.append(Agent(task, self.depth+1).run())
            return self.merge_queries(responses)

    
if __name__ == '__main__':
    test = Agent("My company is looking at entering the electric vehicle market. How should we go about this?", 0)
    print(test.run())