from personalized_health_and_fitness_plan_generator.workflow import personalized_fitness_plan

user_profile = (
    "Age: 28, Gender: Male, Weight: 80kg, Height: 180cm. "
    "Goals: Build lean muscle, improve overall fitness, and enhance flexibility. "
    "Preferences: Enjoys bodyweight workouts, has access to basic home gym equipment, "
    "and prefers a diet that is high in protein with moderate carbs."
)
    

def stream():
    for step in personalized_fitness_plan.stream(user_profile, stream_mode = "updates"):
        print("Personalized Health & Fitness Plan:\n")
        print(step)
        print("\n")
