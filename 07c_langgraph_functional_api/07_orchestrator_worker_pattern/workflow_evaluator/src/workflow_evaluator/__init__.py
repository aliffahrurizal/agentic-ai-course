from workflow_evaluator.workflow import evaluate_prompt

def stream():
    input_state = {
        "prompt_to_evaluate": (
            "You are a dentist receptionist assistant. Your task is to guide users for inquiries related to appointment scheduling and patient inquiries."
        ),
        "gold_standard": (
            "The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, "
            "and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). "
            "It should be concise, clear, and professional."
        ),
        "persona_runs": 2
    }
    for step in evaluate_prompt.stream(input=input_state, stream_mode="updates"):
        print(step)
        print("\n")
