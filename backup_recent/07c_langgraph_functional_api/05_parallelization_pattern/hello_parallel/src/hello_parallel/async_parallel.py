import asyncio
from langgraph.func import entrypoint, task
import time

@task
async def add_ten(num: int) -> dict:
    """Add 10 to the input number."""
    print(f"Starting addition operation on {num}")
    await asyncio.sleep(2)  # Simulate work
    result = num + 10
    print(f"Addition complete: {num} + 10 = {result}")
    return {"operation": "add", "result": result}

@task
async def multiply_by_two(num: int) -> dict:
    """Multiply the input number by 2."""
    print(f"Starting multiplication operation on {num}")
    await asyncio.sleep(2)  # Simulate work
    result = num * 2
    print(f"Multiplication complete: {num} × 2 = {result}")
    return {"operation": "multiply", "result": result}

@task
async def divide_by_self(num: int) -> dict:
    """Divide the number by itself."""
    print(f"Starting division operation on {num}")
    await asyncio.sleep(2)  # Simulate work
    result = num / num if num != 0 else "undefined"
    print(f"Division complete: {num} ÷ {num} = {result}")
    return {"operation": "divide", "result": result}

@entrypoint()
async def process_number(num: int) -> dict:
    """Process a single number with multiple operations in parallel."""
    print(f"\nStarting parallel operations on number: {num}")
    start_time = time.time()
    
    # Run all operations in parallel
    operations = [
        add_ten(num),
        multiply_by_two(num),
        divide_by_self(num)
    ]
    
    results = await asyncio.gather(*operations)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Format results into a dictionary
    results_dict = {
        "input": num,
        "processing_time": f"{processing_time:.2f} seconds",
        "operations": {r["operation"]: r["result"] for r in results}
    }
    
    print(f"\nAll operations completed in {processing_time:.2f} seconds!")
    return results_dict

def run_async_workflow():
    """Function to run the async workflow."""
    result = asyncio.run(process_number.ainvoke(5))
    print("\nFinal Results:")
    print(f"Input number: {result['input']}")
    print(f"Processing time: {result['processing_time']}")
    print("Results:")
    for op, res in result['operations'].items():
        print(f"  {op}: {res}")
    return result 