**Crew, Agent, Flow & Process -- When to use What ?**
=====================================


CrewAI offers multiple ways to structure AI workflows, including using **only an agent**, **a crew of agents**, and organizing execution with **flows and processes**. Below is a breakdown of when and how to use them, along with real-world use cases and examples.

* * *

**1\. Using Only an Agent (`Agent`)**
=====================================

**When to Use**
---------------

* When you need a **single** AI-powered role with a clear goal and responsibilities.
* The task does not require multiple AI agents collaborating.
* Example: A **customer support chatbot** that answers queries without delegation.

**Use Case: AI Legal Assistant**
--------------------------------

Imagine you need an AI **Legal Consultant** that can analyze a given contract and provide insights. This is a single-agent task.

### **Example Code**

```python
from crewai import Agent, Task

# Define the AI Legal Assistant
legal_assistant = Agent(
    role="Legal Consultant",
    goal="Analyze legal contracts and provide a summary with key risk factors.",
    backstory="A seasoned legal consultant specializing in contract analysis and compliance.",
    verbose=True
)

# Define the task for the agent
contract_analysis_task = Task(
    description="Read the contract and summarize key terms and risks.",
    expected_output="A 3-paragraph summary with key terms and risks.",
    agent=legal_assistant
)

# Execute task
result = contract_analysis_task.execute()
print(result)` 
```
🔹 **Why use only an agent?**

* The job is self-contained and does not need multiple agents with different expertise.

* * *

**2\. Using `Crew` (Multiple Agents)**
======================================

**When to Use**
---------------

* When tasks require **multiple roles working together** to accomplish a goal.
* Each agent has a **different responsibility** and they might need to share information.
* Example: A **content creation team** where a researcher gathers info, and a writer crafts the final content.

**Use Case: AI Content Team**
-----------------------------

Imagine an **AI research and writing team** where:  
🔹 **Researcher** finds AI industry trends.  
🔹 **Writer** crafts an engaging blog post.

### **Example Code**

```python
from crewai import Agent, Task, Crew, Process

# Define the Researcher agent
researcher = Agent(
    role="Tech Researcher",
    goal="Discover and summarize the latest AI trends.",
    backstory="An AI expert who keeps up with the latest innovations.",
    verbose=True
)

# Define the Writer agent
writer = Agent(
    role="Content Writer",
    goal="Write a blog post based on research findings.",
    backstory="A writer passionate about making AI accessible to everyone.",
    verbose=True
)

# Research Task
research_task = Task(
    description="Find the latest AI trends and provide a structured summary.",
    expected_output="A structured summary of 3 AI trends.",
    agent=researcher
)

# Writing Task
write_task = Task(
    description="Write a blog post based on the AI research findings.",
    expected_output="A well-structured blog post in markdown format.",
    agent=writer
)

# Define the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Ensures research is done before writing
)

# Execute
result = crew.kickoff()
print(result)` 
```
🔹 **Why use Crew?**

* Tasks are split across **multiple roles** that work together sequentially.

* * *

**3\. Using `Flow` (Task Execution Control)**
=============================================

**When to Use**
---------------

* When you need **structured execution** of tasks, but the workflow might be non-linear.
* You want to **connect agents and tasks flexibly** rather than just running them in a list.
* Example: **Hiring Process** where candidates go through different steps based on screening.

**Use Case: AI Recruitment Process**
------------------------------------

Imagine an **AI-driven hiring pipeline** with:  
🔹 **Screener Agent** reviewing resumes.  
🔹 **Interviewer Agent** conducting technical interviews.  
🔹 **Final Decision Agent** making hiring decisions.

### **Example Code**

```python
`from crewai import Agent, Task, Crew, Flow

# Define Agents
screener = Agent(
    role="Resume Screener",
    goal="Screen resumes and filter candidates based on job criteria.",
    backstory="An HR expert with years of experience in shortlisting candidates.",
    verbose=True
)

interviewer = Agent(
    role="Technical Interviewer",
    goal="Conduct technical interviews and assess candidates' skills.",
    backstory="A senior engineer evaluating candidate expertise.",
    verbose=True
)

decision_maker = Agent(
    role="Hiring Manager",
    goal="Make a final hiring decision based on interviews.",
    backstory="An executive ensuring the best candidate is selected.",
    verbose=True
)

# Define Tasks
screening_task = Task(
    description="Review resumes and shortlist candidates.",
    expected_output="A list of top 5 candidates.",
    agent=screener
)

interview_task = Task(
    description="Conduct interviews with shortlisted candidates.",
    expected_output="A report summarizing interview scores.",
    agent=interviewer
)

final_decision_task = Task(
    description="Analyze interview reports and select the best candidate.",
    expected_output="The name of the selected candidate with justification.",
    agent=decision_maker
)

# Define Flow (Non-linear Execution)
flow = Flow()
flow.add_task(screening_task)
flow.add_task(interview_task, depends_on=[screening_task])  # Interview happens after screening
flow.add_task(final_decision_task, depends_on=[interview_task])  # Decision after interview

# Define Crew with Flow
crew = Crew(agents=[screener, interviewer, decision_maker], tasks=[screening_task, interview_task, final_decision_task], flow=flow)

# Execute
result = crew.kickoff()
print(result)` 
```
🔹 **Why use Flow?**

* It **controls execution dependencies**, ensuring proper sequencing.
* Unlike a simple **sequential process**, Flow allows **non-linear execution** paths.

* * *

**4\. Using `Process` (Execution Mode)**
========================================

**When to Use**
---------------

* Controls **how tasks in a crew execute**:
    * `Process.sequential`: Tasks execute **one after another** (default).
    * `Process.parallel`: Tasks run **at the same time** (if independent).
* Example: **Multiple tasks that can be executed in parallel** (e.g., sentiment analysis for different social media platforms).

**Use Case: Social Media Analysis**
-----------------------------------

Imagine a **social media monitoring crew** where:  
🔹 **Twitter Analyst** processes Twitter sentiment.  
🔹 **Reddit Analyst** processes Reddit discussions.  
🔹 **YouTube Analyst** processes video comments.

Since all tasks are independent, they can run **in parallel**.

### **Example Code**

```python
from crewai import Agent, Task, Crew, Process

# Define Agents
twitter_analyst = Agent(role="Twitter Analyst", goal="Analyze sentiment from Twitter.", verbose=True)
reddit_analyst = Agent(role="Reddit Analyst", goal="Analyze sentiment from Reddit.", verbose=True)
youtube_analyst = Agent(role="YouTube Analyst", goal="Analyze sentiment from YouTube.", verbose=True)

# Define Tasks
twitter_task = Task(description="Analyze sentiment of tweets about a topic.", expected_output="Sentiment score.", agent=twitter_analyst)
reddit_task = Task(description="Analyze sentiment of Reddit discussions.", expected_output="Sentiment score.", agent=reddit_analyst)
youtube_task = Task(description="Analyze sentiment of YouTube comments.", expected_output="Sentiment score.", agent=youtube_analyst)

# Define Crew with Parallel Execution
crew = Crew(
    agents=[twitter_analyst, reddit_analyst, youtube_analyst],
    tasks=[twitter_task, reddit_task, youtube_task],
    process=Process.parallel  # Run all sentiment analyses at the same time
)

# Execute
result = crew.kickoff()
print(result)` 
```
🔹 **Why use `Process.parallel`?**

* Tasks **don't depend on each other**, so they can run simultaneously.

* * *

**Conclusion**
==============

| Component | When to Use | Example Use Case |
| --- | --- | --- |
| **Agent** | Single AI role | Contract Review |
| **Crew** | Multiple collaborating agents | Research + Writing |
| **Flow** | Non-linear workflows | Hiring Process |
| **Process** | Control execution (sequential/parallel) | Social Media Analysis |

Each component provides different levels of **control and flexibility**, depending on the complexity of your use case. 🚀
