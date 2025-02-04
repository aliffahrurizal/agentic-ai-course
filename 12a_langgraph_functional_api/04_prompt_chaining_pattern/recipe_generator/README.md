# Recipe Generation Agent

## Overview

This project is a recipe generation agent that leverages large language models (LLMs) to transform a simple list of available ingredients into a complete recipe. The agent guides the process in multiple steps:

- **Ingredient Analysis:** The agent first analyzes the input list of ingredients to extract flavor profiles, textures, and potential dish ideas.
- **Cuisine Suggestion:** It then uses the analysis to suggest a cuisine that best fits the provided ingredients.
- **Recipe Generation:** Finally, the agent generates a detailed recipe inspired by the suggested cuisine and incorporating the original ingredients.

The result is an end-to-end solution that automates the creative process of recipe generation, making it ideal for users who want to experiment in the kitchen without spending too much time on brainstorming.

## How Prompt Chaining is Used

The project implements the **prompt chaining** pattern by decomposing the overall task into a sequence of smaller, interdependent subtasks. Each step is handled by a dedicated function (or “task”), and the output from one task is used as the input for the next. Here's how the pattern is applied:

1. **Sequential Subtasks:**
   - **Analyze Ingredients:** The first task sends a prompt to the LLM with the list of ingredients. The LLM returns an analysis of the ingredients, including potential flavor profiles and pairing ideas.
   - **Suggest Cuisine:** Next, the analysis is fed into a second prompt that asks the LLM to recommend a suitable cuisine based on the insights gathered.
   - **Generate Recipe:** Finally, both the original list of ingredients and the suggested cuisine are provided in a third prompt to generate a complete recipe with instructions and serving suggestions.

2. **Handoff Between Prompts:**  
   Each task is designed to produce output that is precisely formatted for the subsequent prompt. This controlled handoff ensures that the context is maintained throughout the chain and that each step builds logically on the previous one.

3. **Enhanced Accuracy and Creativity:**  
   By splitting the recipe generation process into clear, focused stages, the agent can fine-tune the creative output at each step. This modular approach allows for easier debugging and refinement compared to a single, monolithic prompt, ultimately leading to a more accurate and engaging final recipe.

## Usage

To run the agent, simply provide a comma-separated list of ingredients. You can change the intial prompt in `main()` or `stream()` functions in `__init__.py`.


---


## How to Run Locally

### Prerequisites

- Python 3.10 or higher
- API Key from Google AI Studio 
- [uv](https://github.com/panaverisity/uv) (our preferred command-line runner)

### Installation

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/panaverisity/learn-agentic-ai.git
   ```

2.1 **Navigate to the Project Directory**

   ```bash
   cd /learn-agentic-ai/12a_langgraph_functional_api/04_prompt_chaining_pattern/recipe_generator
   ```

2.2 **Navigate to the Project Directory**
  Rename .env.example to .env and add GOOGLE_API_KEY. Optionally you can setup the LangChain Variables for tracing in langsmith.

3. **Install Required Packages**

   ```bash
   uv sync
   ```

### Running the Workflow with Python


```bash
uv run invoke
```

```bash
uv run stream
```

---