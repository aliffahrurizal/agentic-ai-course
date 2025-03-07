from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai import LLM

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm1 = LLM(model="ollama/deepseek-r1:1.5b", base_url="http://localhost:11434")
llm2 = LLM(model='gemini/gemini-2.0-flash')

@CrewBase
class DevCrew:
   
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    
    @agent
    def junior_python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["junior_python_developer"],
            
        )
    
    @agent
    def senior_python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_python_developer"],
            llm=llm2
        )

    @task
    def write_code(self) -> Task:
        return Task(
            config=self.tasks_config["write_code"],
        )
    
    @task
    def review_code(self) -> Task:
        return Task(
            config=self.tasks_config["review_code"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
