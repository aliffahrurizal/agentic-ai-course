# REACT Agents in LangGraph

REACT (Reason + Act) is a powerful pattern for building agents that can break down complex tasks through reasoning and acting. In LangGraph, you have two main approaches to implementing REACT agents:

Note: You can try both in react-agent directory
- clone and add GOOGLE_API_KEY in .env file
- ` uv run prebuilt` 
```bash
mjs@Muhammads-MacBook-Pro-3 react-agent % uv run prebuilt
================================ Human Message =================================

What is the capital of the moon?
================================== Ai Message ==================================

The Moon doesn't have a capital city because it's not a country or a self-governing entity.  It's a natural satellite of Earth.
```
- `uv run custom`

## 1. Ussing Prebuilt REACT Agent

LangGraph provides a prebuilt REACT agent implementation that you can use out of the box. This is the recommended approach for most use cases as it implements best practices and common patterns.

To use the prebuilt REACT agent:

```python
!pip install --quiet -U langchain-google_genai langgraph python-dotenv

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Create the agent
agent = create_react_agent(
    model=llm,
    tools=[],
    prompt="You are a helpful assistant..."
)


# Use the agent
response = agent.invoke({
    "messages": [("user", "hi")]
})
```

## 2. Creating Custom REACT Agents

For more specialized use cases, you can create your own REACT agent implementation. This gives you full control over the agent's behavior, reasoning process, and tool usage.

Use this Guide: [How to create a ReAct Agent from Scratch using LangGraph Functional API?](https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch-functional/?h=functional)

## Resources for Learning More

- [LangGraph Documentation on REACT Agents](https://python.langchain.com/docs/langgraph)
- [ReAct Pattern Overview](https://arxiv.org/abs/2210.03629)

## Best Practices

1. Start with the prebuilt agent unless you have specific requirements that it doesn't meet
2. When creating custom agents, follow the ReAct pattern of alternating between reasoning and acting
3. Implement proper error handling and validation
4. Consider adding monitoring and logging for production use
5. Test your agent implementation thoroughly with various inputs
