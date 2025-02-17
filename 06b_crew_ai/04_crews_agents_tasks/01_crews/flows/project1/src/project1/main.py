#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start  # type: ignore

from project1.crews.poem_crew.poem_crew import PoemCrew

from project1.crews.poem_crew.agentia_crew import AgentiaCrew





class AgentiaFlow(Flow):
    @start()
    def code_generation(self):
        print("Generating code")
        result = (
            AgentiaCrew()
            .crew()
            .kickoff(inputs={"requirements": "write for loop to print hello world 10 times"})
        )


def run_agentia_flow():
    agentia_flow = AgentiaFlow()
    agentia_flow.kickoff()







class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class PoemFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Saving poem")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
