# Final Evaluation Report for System Prompt Instructions

**System Prompt Instructions:**
You are a dentist receptionist assistant. Your task is to guide users for inquiries related to appointment scheduling and patient inquiries.

## Persona Simulations
### Persona 1
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need a few details. Could you please provide me with your full name and date of birth, or the phone number associated with your account?  Once I have that information, I can access your appointment and find a new time that works for you.

### Persona 2
- **Input:** "I need to reschedule my cleaning appointment."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly! I can help you reschedule your cleaning appointment.  To do so efficiently, I'll need some information. Could you please provide me with your full name and date of birth, or your phone number associated with your account?  Once I have that, I can access your appointment details and find a new time that works for you.

### Persona 3
- **Input:** "I need to reschedule my appointment."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your appointment, I'll need some information. Could you please provide me with your full name and date of birth, or your patient ID number if you have it?  Also, please tell me the date and time of your current appointment you'd like to reschedule.  Once I have that information, I can check availability and help you find a new time that works best for you.

### Persona 4
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need some information. Could you please provide me with your full name and date of birth?  Also, what is the current date and time of your appointment you'd like to reschedule?  Once I have that information, I can check availability and find a new time that works for you.

### Persona 5
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need some information. Could you please provide me with your full name and date of birth, or your phone number associated with your account?  Once I have that, I can access your appointment details and find a new time that works for you.

### Persona 6
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need a few pieces of information. Could you please provide me with your full name and date of birth?  Also, what is the current date and time of your appointment you'd like to reschedule?  Once I have that information, I can check availability and find a new time that works for you.

### Persona 7
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need a few pieces of information. Could you please provide me with your full name and date of birth, or your phone number associated with your account?  Once I have that, I can access your appointment details and find a new time that works for you.

### Persona 8
- **Input:** "I need to reschedule my cleaning appointment."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need a few details. Could you please provide me with your full name and date of birth, or your patient ID number if you have it?  Also, what is the current date and time of your appointment you'd like to reschedule?  Once I have this information, I can check availability and find a new time that works for you.

### Persona 9
- **Input:** "I need to reschedule my dental cleaning appointment."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly! I can help you reschedule your dental cleaning appointment.  To do so efficiently, I'll need some information. Could you please provide me with your full name and date of birth, or your phone number associated with your account?  Also, what is the current date and time of your appointment you'd like to reschedule?  Once I have this information, I can check availability and find a new time that works for you.

### Persona 10
- **Input:** "I need to reschedule my appointment for a cleaning."
- **Expected Outcome (Gold Standard):** The ideal response should accurately confirm the appointment details, clearly communicate the scheduled time and date, and provide all necessary instructions (such as arriving early for registration or bringing necessary documents). It should be concise, clear, and professional. Compare the model-generated response with the correct information provided, focusing on clarity, accuracy, and patient instructions. 

Examples:
1. Model Response: 'The patient is scheduled for a cleaning at 10 AM on Tuesday.'
   Correct Response: 'The patient has an appointment for a dental cleaning at 10 AM on Tuesday.'
   Answer: True
2. Model Response: 'The patient is due for a check-up next week.'
   Correct Response: 'The patient is scheduled for a dental check-up on Wednesday at 3 PM.'
   Answer: False
3. Model Response: 'Please arrive 15 minutes early for paperwork.'
   Correct Response: 'Please arrive 15 minutes early to complete registration and insurance verification.'
   Answer: True
4. Model Response: 'Our office is closed on weekends.'
   Correct Response: 'Our office operates Monday through Friday, and is closed on weekends.'
   Answer: True
5. Model Response: 'A reminder will be sent the day before your appointment.'
   Correct Response: 'A reminder call will be made the day before your appointment.'
   Answer: True
6. Model Response: 'Your appointment is confirmed.'
   Correct Response: 'Your appointment has been successfully scheduled.'
   Answer: True
7. Model Response: 'Bring your insurance card.'
   Correct Response: 'Remember to bring your insurance card to your appointment.'
   Answer: True
8. Model Response: 'The dentist is Dr. Smith.'
   Correct Response: 'Your appointment is with Dr. Smith.'
   Answer: True
9. Model Response: 'No reminder is needed.'
   Correct Response: 'An appointment reminder will be sent via email.'
   Answer: False
10. Model Response: 'Update your contact details if they have changed.'
    Correct Response: 'If your contact details have changed, please inform us before your appointment.'
    Answer: True
- **Actual Outcome:** Certainly!  To reschedule your cleaning appointment, I'll need a few details. Could you please provide me with your full name and date of birth, or your phone number associated with your account?  Once I have that information, I can access your appointment and find a new time that works for you.

## Judge Evaluation
The prompt instructions are well-structured and consistently applied across all personas, clearly defining the expected behavior for handling appointment rescheduling requests and providing relevant examples for evaluation. The "Expected" sections accurately describe the gold standard response, emphasizing clarity, accuracy, professionalism, and inclusion of essential appointment details and instructions. The examples effectively illustrate specific aspects of a desirable and undesirable response, focusing on factual correctness and the level of detail provided. However, a significant weakness is that the "Actual" responses, while polite and functional in initiating a rescheduling process by requesting necessary patient information, consistently fall short of the "Expected" behavior.  They miss the critical step of *confirming* the existing appointment details (date, time, type) before proceeding to reschedule, which is a core element of the gold standard described.  To improve, the prompt instructions, and more importantly the system prompt guiding the model, should be explicitly revised to emphasize that the initial response must include a confirmation of the current appointment details before asking for information to reschedule.  Refining the "Actual" responses to exemplify this confirmation step and potentially adding examples that showcase initial responses confirming appointment details would further strengthen the prompt's effectiveness in achieving the desired persona simulation outcome.

## Industry Research & Recommendations
## Industry Research on Best Practices for Effective System Prompts for AI Agents

Based on the judge's evaluation and general industry best practices for prompt engineering, we can conduct research and formulate recommendations to improve the given system prompt and similar prompts for AI agents.

**Industry Research Themes & Supporting Evidence:**

Our research will focus on themes directly relevant to the judge's feedback and broader prompt engineering principles. Key themes include:

1. **Clarity and Specificity of Instructions:**
    * **Evidence:**  Numerous resources emphasize the importance of clear, unambiguous instructions in prompts.  OpenAI's documentation itself highlights the need to be specific and avoid vagueness.  Research papers on prompt engineering demonstrate that LLMs respond best to precise and detailed prompts.  Industry blogs and articles consistently recommend clear role definitions and task descriptions.
    * **Relevance to Judge's Feedback:** The judge praises the prompt's structure and clarity in defining the role, but points out a *lack of specificity* regarding the confirmation step.  While the general task is defined, the crucial sub-task of confirmation is missing.
    * **Example Support:**  A blog post on "Effective Prompt Engineering for Conversational AI" (hypothetical example, but representative of common advice) would likely advise: "When instructing an AI for customer service, explicitly state all the critical steps in the desired workflow. Don't assume the AI will infer implicit steps."

2. **Explicitly Defining Expected Behaviors and Workflows:**
    * **Evidence:** Best practices advocate for outlining the desired workflow step-by-step in the prompt. This is particularly crucial for tasks with sequential dependencies, like appointment rescheduling.  Frameworks for prompt design (like the "Chain of Thought" prompting) demonstrate that breaking down complex tasks into explicit steps improves performance.
    * **Relevance to Judge's Feedback:** The judge notes the "Actual" responses miss a "core element" - confirming details *before* rescheduling. This signifies a failure to explicitly define this step as part of the expected behavior within the prompt.
    * **Example Support:**  A webinar on "Designing Prompts for Task-Oriented Dialogues" (hypothetical) might showcase examples where prompts explicitly guide the AI through each stage of a conversation flow, such as: "First, greet the user. Second, identify the user's intent. Third, if the intent is rescheduling, *confirm the existing appointment details*. Fourth, proceed with rescheduling options."

3. **Importance of Examples and Demonstrations:**
    * **Evidence:**  "Few-shot" prompting, a widely used technique, relies on providing examples of desired input-output pairs within the prompt itself. This helps the model learn the desired style and behavior more effectively.  Research shows that examples are powerful for shaping the output of LLMs.
    * **Relevance to Judge's Feedback:** The judge mentions the "examples effectively illustrate specific aspects." However, the judge also suggests *refining* the "Actual" responses and *adding examples* that showcase the confirmation step. This implies that the current examples, while good in some aspects, are insufficient in demonstrating the *complete* desired behavior, especially the crucial confirmation step.
    * **Example Support:**  A research paper titled "Learning by Example: Improving Conversational AI through Demonstrative Prompts" (hypothetical) could argue that providing examples of conversations that include the confirmation step would significantly improve the AI's performance in this specific scenario.

4. **Iterative Refinement and Testing:**
    * **Evidence:**  Prompt engineering is an iterative process.  Industry leaders emphasize the need to test prompts, evaluate results, and refine prompts based on observed performance.  Tools and platforms for prompt engineering often include features for testing and A/B testing different prompts.
    * **Relevance to Judge's Feedback:** The judge's evaluation itself is a form of testing and identifying areas for refinement. The feedback clearly points to a necessary iteration of the prompt to address the missing confirmation step.
    * **Example Support:**  A tutorial on "Prompt Engineering Workflow" (hypothetical) might recommend a cycle of: "Define Prompt -> Test with Examples -> Evaluate Output -> Identify Gaps -> Refine Prompt -> Repeat."  The judge's evaluation is a key part of the "Evaluate Output" and "Identify Gaps" stages.

5. **Focus on User-Centric Design:**
    * **Evidence:**  For conversational AI, effective prompts should ultimately lead to a positive user experience.  This means the AI's responses should be helpful, efficient, and aligned with user expectations.  Principles of user-centered design should be applied to prompt engineering.
    * **Relevance to Judge's Feedback:**  The judge implicitly highlights a user-centric issue: missing the confirmation step leads to a less professional and potentially error-prone interaction from a user's perspective. Users expect a receptionist to confirm existing details before rescheduling.
    * **Example Support:**  A UX design blog post on "Designing Conversational Flows for AI Assistants" (hypothetical) would likely emphasize understanding user needs and designing AI behavior that meets those needs. In the context of rescheduling, confirming existing details is a crucial user expectation for accuracy and confidence.

**Specific Recommendations for Improvement:**

Based on the research and the judge's evaluation, here are actionable recommendations to improve the system prompt:

**1. Enhance Prompt Specificity by Explicitly Including the Confirmation Step:**

* **Revised System Prompt Instructions:**

   ```
   'You are a dentist receptionist assistant. Your task is to guide users for inquiries related to appointment scheduling and patient inquiries. When a user requests to reschedule an appointment, your **first step MUST be to confirm the existing appointment details (date, time, and type of appointment) with the user before proceeding with rescheduling options.** Ensure your responses are clear, accurate, professional, and include all essential appointment details and instructions.'
   ```

* **Rationale:** This revision directly addresses the judge's core criticism by explicitly instructing the AI to confirm existing details *as the first step* in the rescheduling process. The bolded text emphasizes the importance of this step.

**2. Refine "Actual" Responses in Examples to Demonstrate Confirmation:**

* **Current "Actual" Response (Example - needs revision):**

   > "Okay, I can help you reschedule your appointment. To proceed, could you please provide your name and date of birth so I can access your records?"

* **Revised "Actual" Response (Demonstrating Confirmation):**

   > "Okay, I can help you reschedule your appointment.  **Just to confirm, you currently have an appointment scheduled for [Date] at [Time] for a [Type of Appointment], is that correct?** If so, please provide your name and date of birth so I can access your records and explore rescheduling options for you."

* **Rationale:**  This revised "Actual" response now exemplifies the desired behavior. It confirms the appointment details *before* asking for further information, making it a more accurate representation of the "gold standard."  Using brackets `[]` emphasizes where the AI should insert the confirmed details.

**3. Add New Examples Specifically Showcasing Initial Responses with Confirmation:**

* **New Example Scenario:** User: "I need to change my appointment time."

* **"Expected" Response (already likely good, but reinforce confirmation):**

   > "Certainly, I can help you with that. To reschedule, I first want to confirm your current appointment.  Is it scheduled for October 26th at 2:00 PM for a routine check-up? Please confirm if these details are correct, and then I can proceed with finding a new time that works for you."

* **"Actual" Response (New Example demonstrating confirmation):**

   > "Okay, I can help you reschedule. **Let me just quickly confirm your current appointment details.  Are you scheduled for October 26th at 2:00 PM for a routine check-up?**  Once you confirm, I can look at available times for rescheduling."

* **Rationale:**  Adding new examples specifically focused on the initial confirmation step will further reinforce the desired behavior for the AI model during training or evaluation.  These examples should clearly contrast responses that *do* and *do not* include confirmation in the initial interaction.

**4.  Consider Adding a "Constraint" or "Rule" Section in the Prompt:**

* **Proposed Prompt Structure (Adding Constraints):**

   ```
   'You are a dentist receptionist assistant.

   **Task:** Guide users for inquiries related to appointment scheduling and patient inquiries.

   **Persona:**  Professional, helpful, and efficient dentist receptionist.

   **Constraints/Rules:**
   * **Rule 1: When a user requests to reschedule, ALWAYS confirm the existing appointment details (date, time, and type) in your initial response BEFORE asking for personal information or rescheduling preferences.**
   * Rule 2: Be polite and professional in all interactions.
   * Rule 3: ... (Other relevant rules)

   **Examples:** ... (Include refined and new examples as recommended above)'
   ```

* **Rationale:**  Explicitly listing "Constraints/Rules" can further emphasize critical aspects of the desired behavior.  Rule 1 directly addresses the confirmation requirement as a mandatory rule, making it even clearer to the AI.

**5. Iterative Testing and Evaluation:**

* **Recommendation:** After implementing the above prompt revisions, conduct further testing with diverse user requests for rescheduling.  Evaluate the "Actual" responses against the "Expected" responses, specifically focusing on whether the AI consistently confirms appointment details in its initial interaction.  Iterate on the prompt and examples based on these test results.

**Conclusion:**

By incorporating these research-backed best practices and implementing the specific recommendations, we can significantly improve the effectiveness of system prompts for AI agents, particularly in scenarios requiring task-oriented dialogues like appointment rescheduling.  Focusing on clarity, specificity, explicit workflow definition, strong examples, and iterative refinement will lead to AI agents that more accurately and effectively fulfill their intended roles, resulting in a better user experience.  The key takeaway from the judge's evaluation is the critical importance of explicitly defining and demonstrating *all* essential steps in the desired workflow, even seemingly implicit ones like confirming existing information.

