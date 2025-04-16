import asyncio
import os
from typing import AsyncGenerator, List, Sequence, cast, Union
from dotenv import load_dotenv
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response, TaskResult
from autogen_agentchat.messages import TextMessage, ChatMessage, AgentEvent
from autogen_core import CancellationToken, Image
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

class LATSReasoningAgent(BaseChatAgent):
    """
    A custom LATS reasoning agent that implements a tree search with immediate reflection.
    Uses Gemini model for generating and evaluating reasoning steps.
    """
    def __init__(self, name: str, max_depth: int = 3, beam_size: int = 2):
        super().__init__(name, "A LATS reasoning agent with immediate reflection feedback")
        self._max_depth = max_depth
        self._beam_size = beam_size
        self.tree: List[tuple[int, str]] = []
        
        # Initialize model client
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.0-flash",
            api_key=str(gemini_api_key)
        )

    async def _generate_with_model(self, prompt: str) -> str:
        """Generate response using Gemini model directly."""
        response = await self.model_client.create(
            messages=[UserMessage(content=prompt, source="user")]
        )
        return str(response.content) if hasattr(response, 'content') else str(response)

    async def _generate_candidate(self, question: Union[str, List[Union[str, Image]]], depth: int, candidate_index: int) -> str:
        """Generate a reasoning step using the Gemini model."""
        # Handle different types of question content
        if isinstance(question, list):
            question_str = " ".join(str(item) for item in question if not isinstance(item, Image))
        else:
            question_str = str(question)

        prompt = f"""As a reasoning agent, generate a thoughtful step in analyzing this question: "{question_str}"
        This is step {depth + 1} in the reasoning process.
        Focus on one specific aspect and provide clear logical connections.
        Use phrases like 'because', 'therefore', 'however', and 'specifically' to show your reasoning.
        Previous steps have covered: {self.tree[-3:] if self.tree else 'No previous steps'}.
        """
        return await self._generate_with_model(prompt)

    async def _grade_candidates(self, candidates: List[TextMessage]) -> TextMessage:
        """Grade candidates using the Gemini model for evaluation."""
        all_candidates = "\n".join(f"Candidate {i+1}: {c.content}" for i, c in enumerate(candidates))
        prompt = f"""Evaluate these reasoning steps and select the best one based on:
        1. Logical coherence
        2. Depth of analysis
        3. Relevance to the question
        4. Use of clear reasoning markers (because, therefore, etc.)

        Candidates:
        {all_candidates}

        Return ONLY the number of the best candidate (1, 2, or 3).
        """
        
        response = await self._generate_with_model(prompt)
        try:
            best_index = int(str(response).strip()) - 1
            return candidates[best_index % len(candidates)]
        except (ValueError, IndexError):
            return candidates[0]

    async def _generate_conclusion(self, history: List[ChatMessage]) -> str:
        """Generate a final conclusion using the Gemini model."""
        # Extract text content safely from history
        reasoning_steps = []
        for msg in history:
            if isinstance(msg.content, str):
                reasoning_steps.append(msg.content)
            elif isinstance(msg.content, list):
                text_content = [str(item) for item in msg.content if not isinstance(item, Image)]
                reasoning_steps.append(" ".join(text_content))
            else:
                reasoning_steps.append(str(msg.content))

        prompt = f"""Based on the following reasoning steps, provide a comprehensive conclusion:

        Question: {reasoning_steps[0] if reasoning_steps else 'No question provided'}
        
        Reasoning steps:
        {chr(10).join(reasoning_steps[1:])}

        Provide a structured conclusion with:
        1. Key findings
        2. Recommendations
        3. Next steps
        """
        
        return await self._generate_with_model(prompt)

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        final_response = None
        async for item in self.on_messages_stream(messages, cancellation_token):
            if isinstance(item, Response):
                final_response = item
        if final_response is None:
            raise AssertionError("No final response produced by LATS reasoning")
        return final_response

    async def on_messages_stream(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[AgentEvent | ChatMessage | Response, None]:
        history: List[ChatMessage] = list(messages)
        current_depth = 0
        question = messages[0].content if messages else "No question provided"

        while current_depth < self._max_depth:
            if cancellation_token.is_cancelled():
                break

            candidates: List[TextMessage] = []
            for i in range(self._beam_size):
                candidate_text = await self._generate_candidate(question, current_depth, i)
                candidate_msg = TextMessage(content=candidate_text, source=self.name)
                candidates.append(candidate_msg)
                self.tree.append((current_depth, candidate_text))

            best_candidate = await self._grade_candidates(candidates)
            history.append(best_candidate)
            yield best_candidate
            current_depth += 1

        final_text = await self._generate_conclusion(history)
        final_msg = TextMessage(content=final_text, source=self.name)
        history.append(final_msg)
        yield Response(chat_message=final_msg, inner_messages=history)

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        self.tree.clear()

# Example usage with a real-world problem:
async def run_lats_agent():
    agent = LATSReasoningAgent("lats_reasoner", max_depth=4, beam_size=3)
    
    test_message = TextMessage(
        content="How can we implement effective error handling in a distributed system?",
        source="user"
    )
    
    print("\nLATS Reasoning Process:")
    print("-" * 50)
    async for output in agent.on_messages_stream([test_message], CancellationToken()):
        if isinstance(output, Response):
            print("\nFinal Response:")
            print("-" * 20)
            print(output.chat_message.content)
        else:
            print(f"\nReasoning Step:")
            print("-" * 15)
            print(output.content)
    
    print("\nReasoning Tree Structure:")
    print("-" * 50)
    for depth, content in agent.tree:
        print(f"{'  ' * depth}└─ {content}")

def call_lats_agent():
    asyncio.run(run_lats_agent())

if __name__ == "__main__":
    call_lats_agent()
