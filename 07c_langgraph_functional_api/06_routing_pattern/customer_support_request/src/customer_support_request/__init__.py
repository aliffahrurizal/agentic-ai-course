from customer_support_request.workflow import customer_support_routing

# customer_query = (
#     "I was charged twice for my recent purchase and need a refund explanation. "
#     "Can someone help me understand these charges?"
# )

customer_query = (
    "My internet connection keeps dropping every few minutes. "
    "I've already tried restarting my router, but the issue persists. "
    "Can you help me troubleshoot this?"
)

def stream():
    for step in customer_support_routing.stream(customer_query, stream_mode="updates"):
        print(step)
        print("\n")


