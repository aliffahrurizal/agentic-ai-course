from typing import Dict, Any, TypedDict

class AgentConfig(TypedDict):
    pass  # Add specific fields if needed

class TaskConfig(TypedDict):
    pass  # Add specific fields if needed

class Agent:
    def __init__(self, config: AgentConfig) -> None: ...

class Task:
    def __init__(self, config: TaskConfig) -> None: ...

class Crew:
    def __init__(self, agents: list[Agent], tasks: list[Task]) -> None: ... 