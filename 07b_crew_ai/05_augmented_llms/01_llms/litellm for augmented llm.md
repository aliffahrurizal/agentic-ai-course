# LLMs

[LLMs Docs](https://docs.crewai.com/concepts/llms)

https://docs.crewai.com/how-to/llm-connections

1. crate flow with crewai `crewai create flow <project_name>`
2. change current directory and open this project on cursor ai (IDE)
    a. `cd <project_name>`
    b. `cursor .` or `code .` 
3. create `src/<project_name>/main1.py`
    * replace <project_name> place holder with your project name.

```python
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

```

2. set `.env` file 
```python
GEMINI_API_KEY=you keys
MODEL=gemini/gemini-2.0-flash
```

3. set command in `.toml` file
```toml
[project.scripts]
simple-llm = "litellm1.main1:run_litellm_flow"
```

4. run project
```cmd
uv run simple-llm
```
