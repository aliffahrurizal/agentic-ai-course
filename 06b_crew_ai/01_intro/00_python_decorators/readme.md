# A Comprehensive Tutorial on Python Decorators

Python decorators are a powerful and elegant feature that allows developers to modify the behavior of a function or a class method without altering its source code. Decorators are widely used in frameworks like CrewAI to enable extensibility, making them an essential concept to master.

## 1. **Understanding the Basics of Python Decorators**

### What is a Decorator?
A decorator is a callable (usually a function) that takes another function as an argument, modifies or extends its behavior, and returns the modified function.


* * *

### **\. Example --Smart Home Automation (Enhancement Decorator)**

* **Function:** Turning on the TV.
* **Before Execution (Decorator):** Adjust room lighting and temperature.
* **Function Execution:** TV turns on and starts playing.
* **After Execution (Decorator):** Adjusts volume based on room noise level.

```python
def smart_home_decorator(func):
    def wrapper():
        # Before execution
        print("Adjusting room lighting...")
        print("Setting optimal temperature...")
        
        # Original function execution
        func()
        
        # After execution
        print("Measuring ambient noise...")
        print("Adjusting TV volume...")
    
    return wrapper

@smart_home_decorator
def turn_on_tv():
    print("TV turning on...")
    print("Starting content playback...")

# Using the decorated function
turn_on_tv()
```
* * *
### Why Use Decorators?
- Code reusability.
- Separation of concerns.
- Clean and maintainable code.

### Syntax of a Decorator
Using the `@decorator_name` syntax:

```python
@decorator_name
def my_function():
    pass
```

This is equivalent to:

```python
def my_function():
    pass

my_function = decorator_name(my_function)
```

---

## 2. **Creating Your First Decorator**

Let’s start with a simple example:

### Example: Logging Decorator

```python
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
```

**Output:**
```
Calling function: say_hello
Hello, Alice!
Function say_hello finished execution
```

---

## 3. **Decorators with Arguments**

To create a decorator that accepts arguments, you need to nest functions further.

### Example: Repeat Function Calls

```python
def repeat(num_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hi {name}!")

greet("Bob")
```

**Output:**
```
Hi Bob!
Hi Bob!
Hi Bob!
```

---

## 4. **Using `functools.wraps`**

When using decorators, metadata like the name and docstring of the original function may be lost. To preserve this information, use `functools.wraps`.

### Example: Preserving Metadata

```python
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def add(a, b):
    """Adds two numbers."""
    return a + b

print(add.__name__)  # Output: add
print(add.__doc__)   # Output: Adds two numbers.
```

---

## 5. **Chaining Multiple Decorators**

You can stack multiple decorators on a single function by applying them one after the other.

### Example: Stacking Decorators

```python
def uppercase_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

def exclamation_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result + "!"
    return wrapper

@uppercase_decorator
@exclamation_decorator
def greet():
    return "hello"

print(greet())  # Output: HELLO!
```

---

## 6. **Class-Based Decorators**

You can also define decorators as classes by implementing the `__call__` method.

### Example: Class-Based Logging Decorator

```python
class LogDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"Calling {self.func.__name__}")
        result = self.func(*args, **kwargs)
        print(f"{self.func.__name__} finished execution")
        return result

@LogDecorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
```

---

## 7. **Real-World Examples of Decorators**

### 7.1 Authentication Decorator

```python
def require_authentication(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("authenticated", False):
            raise PermissionError("User is not authenticated")
        return func(user, *args, **kwargs)
    return wrapper

@require_authentication
def view_profile(user):
    print(f"User profile: {user['name']}")

user = {"name": "Alice", "authenticated": True}
view_profile(user)
```

### 7.2 Timing Decorator

```python
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(2)
    print("Finished")

slow_function()
```

---

## 8. **Tips and Best Practices**

1. **Use `functools.wraps`** to retain metadata of the original function.
2. **Keep Decorators Modular:** Design them to perform a single responsibility.
3. **Document Decorators:** Clearly describe what your decorator does and its intended use.
4. **Test Thoroughly:** Ensure that your decorator works with various types of functions and arguments.

---

By mastering Python decorators, you can write elegant, reusable, and highly extensible code. Frameworks like CrewAI leverage decorators to enable seamless extensibility and modularity, making them a cornerstone of modern Python development. Go ahead and experiment with creating your own decorators—the possibilities are endless!

