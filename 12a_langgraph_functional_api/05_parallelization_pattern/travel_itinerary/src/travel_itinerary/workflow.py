import os
import logging
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

@task
def generate_restaurant_suggestions(location: str) -> str:
    """
    Generate a list of top restaurant recommendations for the given location.
    """
    prompt = (
        f"List 3 highly rated restaurants in {location} known for their diverse cuisine. "
        f"Provide a brief description for each."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_attraction_suggestions(location: str) -> str:
    """
    Generate a list of must-see attractions in the given location.
    """
    prompt = (
        f"List 3 popular tourist attractions in {location}. "
        f"Include a short explanation of what makes each one unique."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_hotel_suggestions(location: str) -> str:
    """
    Generate a list of recommended hotels in the given location.
    """
    prompt = (
        f"List 3 well-reviewed hotels in {location} that offer good value. "
        f"Provide a brief description and mention any unique amenities."
    )
    msg = llm.invoke(prompt)
    return msg.content

@task
def aggregate_itinerary(location: str, restaurants: str, attractions: str, hotels: str) -> str:
    """
    Combine the restaurant, attraction, and hotel suggestions into a cohesive travel itinerary.
    """
    itinerary = f"**Travel Itinerary for {location}**\n\n"
    itinerary += "**Restaurants:**\n" + restaurants + "\n\n"
    itinerary += "**Attractions:**\n" + attractions + "\n\n"
    itinerary += "**Hotels:**\n" + hotels + "\n\n"
    itinerary += "Enjoy your trip and make the most of your adventure!"
    return itinerary

@task
def write_to_file(response: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    response_file_path = os.path.join(output_dir, "travel_itinerary.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response)
    
    return response_file_path

@entrypoint()
def travel_itinerary_workflow(location: str) -> str:
    # Run the three tasks in parallel
    restaurants_future = generate_restaurant_suggestions(location)
    attractions_future = generate_attraction_suggestions(location)
    hotels_future = generate_hotel_suggestions(location)

    # Once all tasks complete, aggregate the results
    final_itinerary = aggregate_itinerary(
        location,
        restaurants_future.result(),
        attractions_future.result(),
        hotels_future.result()
    ).result()
    # Save the final itinerary as a Markdown file
    file_path = write_to_file(final_itinerary).result() 
    return {
        "final_itinerary": final_itinerary,
        "file_path": file_path  # ✅ Now properly returning the file path
    }


