def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} finished execution")
        return result
    return wrapper

@log_decorator
def say_hello(name):
    print(f"Hello, {name}!")

def say_hello_cli():  # Add this function for CLI usage
    say_hello("Alice")  # Now this handles the argument

if __name__ == "__main__":
    say_hello_cli()
