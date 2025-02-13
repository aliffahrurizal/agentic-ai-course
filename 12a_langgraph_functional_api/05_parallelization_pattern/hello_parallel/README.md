# Hello Parallel

A demo of parallel processing patterns in LangGraph using both async and sync approaches.

## Installation

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync
```

## Running the Demos

You can run the demos in several ways:

### Using UV directly

```bash
# Run async version
uv run async-parallel

# Run sync version
uv run sync-parallel
```

## What to Expect

Both demos will:

1. Process 5 numbers (1-5) in parallel
2. Add 2 to each number
3. Include a 2-second delay to simulate work
4. Show progress messages
5. Display total processing time

The total processing time should be around 2 seconds (not 10 seconds) since the operations run in parallel.

```bash
mjs@Muhammads-MacBook-Pro-3 hello_parallel % uv run sync-parallel

Starting parallel operations on number: 5
Starting addition operation on 5
Starting multiplication operation on 5
Starting division operation on 5
Division complete: 5 ÷ 5 = 1.0
Addition complete: 5 + 10 = 15
Multiplication complete: 5 × 2 = 10

All operations completed in 2.00 seconds!

Final Results:
Input number: 5
Processing time: 2.00 seconds
Results:
  add: 15
  multiply: 10
  divide: 1.0
{'input': 5, 'processing_time': '2.00 seconds', 'operations': {'add': 15, 'multiply': 10, 'divide': 1.0}}
mjs@Muhammads-MacBook-Pro-3 hello_parallel % uv run async-parallel

Starting parallel operations on number: 5
Starting addition operation on 5
Starting multiplication operation on 5
Starting division operation on 5
Addition complete: 5 + 10 = 15
Multiplication complete: 5 × 2 = 10
Division complete: 5 ÷ 5 = 1.0

All operations completed in 2.00 seconds!

Final Results:
Input number: 5
Processing time: 2.00 seconds
Results:
  add: 15
  multiply: 10
  divide: 1.0
{'input': 5, 'processing_time': '2.00 seconds', 'operations': {'add': 15, 'multiply': 10, 'divide': 1.0}}
mjs@Muhammads-MacBook-Pro-3 hello_parallel % 

```