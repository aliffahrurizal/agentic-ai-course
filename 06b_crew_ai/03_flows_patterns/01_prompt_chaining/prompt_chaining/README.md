# Prompt Chaining Pattern Flow 

## How to run locally

### Pre-Requisites

- Python 3.10 or higher
- Get your API key from [Goolge AI Studio](https://aistudio.google.com/)
- Add your api key in `.env` file.
-  UV(our preferred command-line runner)

### Installation

1. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/panaverisity/learn-agentic-ai.git
```

2. Navigate to the Project Directory
```bash
cd /learn-agentic-ai/06b_crew_ai/03_flows_patterns/01_prompt_chaining
```

3. Rename .env.example to .env and add GOOGLE_API_KEY.

4. Install required packages
```bash
uv sync
```
5. Run the Flow
```bash
uv run kickoff
```
or
```bash
crewai flow kickoff
```

6. Create the Plot
```bash
uv run plot
```
or
```bash
crewai flow plot
```
