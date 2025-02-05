from crewai.flow.flow import Flow, start, listen
import time


class SimpeFlow(Flow):

    @start()
    def function1(self):
        print("Step1..")
        time.sleep(3)

    @listen(function1)
    def function2(self):
        print("Step2..")
        time.sleep(3)

    @listen(function2)
    def function3(self):
        print("Step3..")
        time.sleep(3)

def kickoff():
    obj = SimpeFlow()
    obj.kickoff()