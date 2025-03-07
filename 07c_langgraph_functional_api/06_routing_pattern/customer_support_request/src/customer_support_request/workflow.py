import os
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# 1. Define the routing schema using a structured output model.
class Route(BaseModel):
    step: Literal["billing", "technical", "general"] = Field(
        None, description="The category for the support request"
    )

# Augment the LLM with the structured output schema for routing.
router = llm.with_structured_output(Route)


# 2. Implement a function to route the customer query.
def llm_call_router(query: str) -> str:
    decision = router.invoke([
        SystemMessage(
            content=(
                "Route the following customer support query into one of these categories: "
                "'billing', 'technical', or 'general'."
            )
        ),
        HumanMessage(content=query),
    ])
    return decision.step


# 3. Create specialized tasks for each support category.
@task
def generate_billing_response(query: str) -> str:
    """
    Generates a response tailored for billing inquiries.
    """
    prompt = (
        f"Customer query: {query}\n\n"
        "Generate a professional response that addresses billing concerns. "
        "Include details on payment issues, refund policies, and account charges."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_technical_response(query: str) -> str:
    """
    Generates a response tailored for technical support issues.
    """
    prompt = (
        f"Customer query: {query}\n\n"
        "Generate a technical support response. Provide clear troubleshooting steps "
        "and advice for resolving technical problems."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_general_response(query: str) -> str:
    """
    Generates a response for general inquiries.
    """
    prompt = (
        f"Customer query: {query}\n\n"
        "Generate a friendly and helpful response for a general customer inquiry. "
        "If needed, advise the customer to contact support for further assistance."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def write_to_file(response: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    response_file_path = os.path.join(output_dir, "customer_support_request.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response)
    return response_file_path
# 4. Create the routing workflow entrypoint.
@entrypoint()
def customer_support_routing(query: str) -> str:
    # Route the customer query to determine the support category.
    next_step = llm_call_router(query)
    
    # Depending on the routing decision, invoke the corresponding task.
    if next_step == "billing":
        response = generate_billing_response(query).result()
    elif next_step == "technical":
        response = generate_technical_response(query).result()
    elif next_step == "general":
        response = generate_general_response(query).result()
    else:
        response = "Sorry, we could not determine the type of your request. Please contact customer support directly."
    
    # Step 4: Save the final plan to a text file.
    file_path = write_to_file(response).result()

    return {
        "final_response": response,
        "file_path": file_path  # ✅ Returning file path instead of None
    }