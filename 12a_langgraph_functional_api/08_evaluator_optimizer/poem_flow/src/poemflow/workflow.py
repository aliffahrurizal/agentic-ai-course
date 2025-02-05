import os
from random import randint
from dotenv import load_dotenv, find_dotenv
from typing import TypedDict, Literal
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

_: bool = load_dotenv(find_dotenv())

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


class PoemFeedback(BaseModel):
    quality: Literal["good", "needs_improvement"] = Field(
        description="Evaluate if the poem is good or needs improvement.",
    )
    feedback: str = Field(
        description="If the poem needs improvement, provide specific feedback on how to enhance it.",
    )


evaluator = model.with_structured_output(PoemFeedback)


class InputState(TypedDict):
    topic: str


@task
def generate_sentence_count() -> int:
    """Generate a random sentence count for the poem."""
    return randint(1, 5)


@task
def generate_poem(sentence_count: int, topic: str, feedback: PoemFeedback = None) -> str:
    """Generate a poem based on the sentence count using the AI model."""
    if feedback:
        prompt = f"""Write a beautiful and engaging poem about {topic} with exactly {sentence_count} sentences.
        Please consider this feedback for improvement: {feedback.feedback}"""
    else:
        prompt = f"""Write a beautiful and engaging poem about {
            topic} with exactly {sentence_count} sentences."""

    response = model.invoke(prompt)
    # Extract string content from the response
    return str(response.content)


@task
def evaluate_poem(poem: str) -> PoemFeedback:
    """Evaluate the quality of the poem."""
    feedback = evaluator.invoke(
        f"""Evaluate this poem:
        {poem}

        Provide feedback on its quality, imagery, emotion, and adherence to poetic elements."""
    )
    return feedback


@task
def save_poem(poem: str) -> str:
    """Save the poem to a file in a correct directory to avoid path errors."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(output_dir, "poem.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(poem)

    return f"Poem saved successfully at {file_path}"


@entrypoint()
def run_workflow(input: InputState):
    """Workflow to generate and save a poem with quality optimization."""
    sentence_count = generate_sentence_count().result()
    topic = input.get("topic", "Random Topic")

    feedback = None
    while True:
        poem = generate_poem(sentence_count, topic, feedback).result()
        feedback = evaluate_poem(poem).result()
        if feedback.quality == "good":
            break

    save_status = save_poem(poem).result()
    return {
        "sentence_count": sentence_count,
        "poem": poem,
        "feedback": feedback.dict(),
        "status": save_status
    }
