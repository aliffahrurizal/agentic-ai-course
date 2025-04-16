from travel_itinerary.workflow import travel_itinerary_workflow

location = "Paris, France"

def stream():
    for step in travel_itinerary_workflow.stream(location, stream_mode="updates"):
        print(step)
        print("\n")
