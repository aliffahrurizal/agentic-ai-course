https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html

https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/messages.html

https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent.on_messages

CancellationToken is used to gracefully cancel an asynchronous operation. In AutoGen, when you call an agent’s methods (like on_messages or run_stream), they might run for a while—especially if they’re processing complex tasks or waiting for responses. By providing a CancellationToken, you have a mechanism to signal that the operation should be aborted, for example, if the user cancels the request or if a timeout occurs.

In our code example, we create a CancellationToken and pass it to the agents. If you call cancellation_token.cancel(), it will cause the ongoing asynchronous operation to raise a cancellation exception, allowing your application to stop processing immediately.

This is very useful for interactive applications where you might need to interrupt a long-running agent task.