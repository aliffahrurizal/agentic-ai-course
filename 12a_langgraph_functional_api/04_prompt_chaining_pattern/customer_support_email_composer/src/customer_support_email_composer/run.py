from customer_support_email_composer.workflow import customer_support_response_workflow

customer_email = (
    "Hi, I recently purchased a laptop from your store, but it has been malfunctioning. "
    "I am very disappointed with the quality and would like to know what can be done about it."
)

def main_run():
    # Run the workflow
    result = customer_support_response_workflow.invoke(customer_email)
    print("\n\n", "Customer Support Email: ", result, "\n\n")
        
def stream_run():
    for step in customer_support_response_workflow.stream(customer_email, stream_mode="updates"):
        print(step)
        print("\n")
    