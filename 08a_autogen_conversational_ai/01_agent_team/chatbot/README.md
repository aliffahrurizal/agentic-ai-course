Give these commands to run the project:

        cd chatbot

        uv venv

    On Mac:

        source .venv/bin/activate

    Using uv to run the project

        uv run chainlit run main.py -h

https://docs.chainlit.io/backend/command-line

This demonstrate how to interact with a single AssistantAgent from the chat interface.

You can use one of the starters. For example, ask "What the weather in Seattle?".

The agent will respond by first using the tools provided and then reflecting on the result of the tool execution.

