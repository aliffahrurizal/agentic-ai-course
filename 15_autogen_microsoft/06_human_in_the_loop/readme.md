# Human-in-the-Loop

Let;s focus on how to interact with the team from your application, and provide human feedback to the team.

There are two main ways to interact with the team from your application:

- During a team’s run – execution of run() or run_stream(), provide feedback through a UserProxyAgent.
- Once the run terminates, provide feedback through input to the next call to run() or run_stream().

https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html

## Run Example Code and Understand the components

1. Clone the code present in console_chat_agent.
2. Add openai_key in .env
3. Run  
```bash
uv run hil
```
4. Continue Chat with the agent in console

Sample Logs

```bash
Hello! How can I assist you today? Feel free to ask me any questions you have.
Enter your response: Hi 
---------- user_proxy ----------
Hi
---------- assistant ----------
Hello! How can I help you today? If you have any questions, feel free to ask!
Enter your response: TERMINATE
---------- user_proxy ----------
TERMINATE
APPR---------- assistant ----------
TERMINATE
Enter your response: APPROVE
---------- user_proxy ----------
APPRAPPROVE
```

Reference Learning Material:
- https://microsoft.github.io/autogen/dev//reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.UserProxyAgent
- https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html
