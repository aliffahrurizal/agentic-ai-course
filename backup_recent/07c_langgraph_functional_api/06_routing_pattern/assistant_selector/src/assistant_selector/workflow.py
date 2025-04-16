from typing import TypedDict, Literal, cast
from pydantic import BaseModel

from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

# Initialize different model instances
router_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b-001")
simple_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
advanced_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
reasoning_coding_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21")


class InputState(TypedDict):
    question: str


QuestionType = Literal["simple", "complex", "code"]

class QuestionClassifier(BaseModel):
    type: QuestionType

@task
def classify_question(question: str) -> QuestionType:
    """Classify the question to determine which model should handle it."""
    prompt = """Analyze the following question and classify it as either:
    - 'simple': For basic, factual, or common questions
    - 'complex': For questions requiring deep analysis, reasoning, or expertise
    - 'code': For questions about programming or technical implementations
    
    Respond with ONLY the classification word.
    
    Question: {question}
    """

    response = cast(QuestionClassifier, router_model.with_structured_output(QuestionClassifier).invoke(prompt.format(question=question)))
    result = response.type

    if result not in ["simple", "complex", "code"]:
        return "complex"  # Default to complex if classification is unclear
    return result  # type: ignore


@task
def handle_simple_question(question: str) -> str:
    """Handle simple questions using the basic model."""
    prompt = f"""Please provide a clear and concise answer to this question: {
        question}"""
    response = simple_model.invoke(prompt)
    return response.content


@task
def handle_complex_question(question: str) -> str:
    """Handle complex questions using the advanced model."""
    prompt = f"""Please provide a detailed, well-reasoned answer to this question: {
        question}"""
    response = advanced_model.invoke(prompt)
    return response.content


@task
def handle_code_question(question: str) -> str:
    """Handle code-related questions using the advanced model with specific instructions."""
    prompt = f"""Please provide a detailed answer with code examples where appropriate.
    Include explanations of the code and best practices.

    Question: {question}"""
    response = reasoning_coding_model.invoke(prompt)
    return response.content


@entrypoint()
def run_workflow(input: InputState):
    """Route the question to the appropriate handler based on classification."""
    question = input.get("question", "")
    question_type = classify_question(question).result()

    if question_type == "simple":
        answer = handle_simple_question(question).result()
    elif question_type == "code":
        answer = handle_code_question(question).result()
    else:  # complex
        answer = handle_complex_question(question).result()

    return {
        "question_type": question_type,
        "answer": answer
    }
