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

say_hello("Alice")