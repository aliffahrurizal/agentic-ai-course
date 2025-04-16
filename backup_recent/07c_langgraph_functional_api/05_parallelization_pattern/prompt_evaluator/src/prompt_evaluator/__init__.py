from prompt_evaluator.workflow import evaluate_prompt

def stream():
    input_state = {
        "prompt_to_evaluate": (
            "You are a dentist receptionist assistant. Your task is to guide users for inquiries related to appointment scheduling and patient inquiries."
        ),
        "gold_standard": (
            "The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, "
            "and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). "
            "It should be concise, clear, and professional. "
            "Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. \n\n"
            "Examples:\n"
            "1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'\n"
            "   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'\n"
            "   Answer: True\n"
            "2. Model Response: 'The patient is due for a check-up next week.'\n"
            "   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'\n"
            "   Answer: False\n"
            "3. Model Response: 'Please arrive 15 minutes early for paperwork.'\n"
            "   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'\n"
            "   Answer: True\n"
            "4. Model Response: 'Our office is closed on weekends.'\n"
            "   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'\n"
            "   Answer: True\n"
            "5. Model Response: 'A reminder will be sent the day before your appointment.'\n"
            "   Correct Response: 'A reminder call will be made the day before your appointment.'\n"
            "   Answer: True\n"
            "6. Model Response: 'Your appointment is confirmed.'\n"
            "   Correct Response: 'Your appointment has been successfully scheduled.'\n"
            "   Answer: True\n"
            "7. Model Response: 'Bring your insurance card.'\n"
            "   Correct Response: 'Remember to bring your insurance card to your appointment.'\n"
            "   Answer: True\n"
            "8. Model Response: 'The dentist is Dr. Smith.'\n"
            "   Correct Response: 'Your appointment is with Dr. Smith.'\n"
            "   Answer: True\n"
            "9. Model Response: 'No reminder is needed.'\n"
            "   Correct Response: 'An appointment reminder will be sent via email.'\n"
            "   Answer: False\n"
            "10. Model Response: 'Update your contact details if they have changed.'\n"
            "    Correct Response: 'If your contact details have changed, please inform us before your appointment.'\n"
            "    Answer: True\n\n"
        ),
        "persona_runs": 10
    }
    for step in evaluate_prompt.stream(input=input_state, stream_mode="updates"):
        print(step)
        print("\n")
