from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv


load_dotenv()


class TopicOutlineFlow(Flow):
    model = 'gemini/gemini-2.0-flash-exp'

    @start()
    def generate_topic(self):
        # Prompt the LLM to generate the a blog topic
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Generate a creative blog topic for 2025."
                }
            ]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        print(f"Generated Topic: {topic}")
        return topic

    @listen(generate_topic)
    def generate_outline(self, topic):
        # Now chain the output by using the topic in a follow-up prompt.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Based on the topic '{topic}', create a detailed outline for a blog post."
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Generated Outline:")
        print(outline)
        return outline


def kickoff():
    prompt_chaining_flow = TopicOutlineFlow()
    final_outline = prompt_chaining_flow.kickoff()
    print("Final Output:")
    print(final_outline)


def plot():
    prompt_chaining_flow = TopicOutlineFlow()
    prompt_chaining_flow.plot()


if __name__ == "__main__":
    kickoff()
    plot()
