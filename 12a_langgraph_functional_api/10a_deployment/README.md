# Deployment Guide for Langgraph Orchestrated Agentic Applications

This guide focuses on the core deployment concepts for your application. We will use:

1. LangGraph Cloud(Server)
2. CrewAI Cloud
3. BentoML
4. FastAPI Server

Deploying an AI Agent is more than an API Call. It's the environment for your agent(s) to operate and create some value. Think of it as Agentic Infrastructure where you manage
- Persistence
- Memory
    - Short Term
    - LongTerm
- Human in the Loop
- Data Storage
- Observability
- Self Healing
- Protocol for Communication with other Agents/APIs/Humans.

## 1. LangGraph Server

LangGraph Platform is a commercial solution for deploying agentic applications in production, built on the open-source LangGraph framework.

- [Concepts](<https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/>)
- [API Spec](<https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref.html#tag/assistants>)
- [API Reference](<https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref/>)

Let's get a quick project setup:
1. Create a new project add langgraph package and add implementation for any Design Pattern or AI Workflow.
2. At root add a langraph.json file with following details. Rename the path to path of your agent.
**Note**- Ensure you have `LANGSMITH_API_KEY` environment variable in .env file. Get the API Key for free from LangSmith Dashboard

```bash
cd langgraph_demo

langgraph_demo % uv run prompt-chain

Processing first step with input: Hello, LangGraph!
Processing second step with input: First step processed: Hello, LangGraph!
{'input': 'Hello, LangGraph!', 'output': 'Second step processed: First step processed: Hello, LangGraph!'}
```

### Setup LangGraph Server

- Add langgraph.json file and update the agent path.
i.e:
```json
{
  "graphs": {
    "chain": "./src/langgraph_demo/prompt_chain.py:entrypoint"
  },
  "env": "./.env",
  "python_version": "3.11",
  "dependencies": [
    "."
  ]
}
```

Now we can just deploy it on their cloud or run locally first

#### 1. Run LangGraph Server Locally

Ensure the docker engine is running and then run the following commands.

```bash
uv pip install langgraph-cli

langgraph up
```

Once setup completes open in bowser:

- Docs: http://127.0.0.1:8123/docs
- [Access Studio](https://langchain-ai.github.io/langgraph/cloud/how-tos/test_local_deployment/#access-studio) in Browser: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123

#### 2. [Deploy on LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/quick_start/)

- Go to [LangSmith](https://smith.langchain.com/)
- Click on `deployments` tab on the left LangSmith panel
- Add `+ New Deployment`
- Then, select the Github repository (e.g., `langchain-academy`) that you just created for the course
- Point the `LangGraph API config file` at one of the `studio` directories
- For example, for module-1 use: `module-1/studio/langgraph.json`
- Set your API keys (e.g., you can just copy from your `module-1/studio/.env` file)

![Screenshot 2024-09-03 at 11.35.12 AM.png](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66dbad4fd61c93d48e5d0f47_deployment2.png)

### Work with your deployment

We can then interact with our deployment a few different ways:

- With the [SDK](https://langchain-ai.github.io/langgraph/cloud/quick_start/#use-with-the-sdk), as before.
- With the [LangGraph Studio](https://langchain-ai.github.io/langgraph/cloud/quick_start/#interact-with-your-deployment-via-langgraph-studio).
