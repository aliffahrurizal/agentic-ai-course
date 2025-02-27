from crewai.flow import Flow, listen, start
from litellm import completion

class LiteLmmFlow(Flow):

    @start()
    def start_function(self):
        output = completion(
            model="gemini/gemini-2.0-flash",
            messages=[
            {'role':'user',
             'content':'who is the founder of Pakistan?'}
        ])
        return output['choices'][0]['message']['content']

def run_litellm_flow():
    obj = LiteLmmFlow()
    result = obj.kickoff()
    print(result)
