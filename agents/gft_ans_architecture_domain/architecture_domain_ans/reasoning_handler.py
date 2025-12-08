# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Gemini 3.0 Thought Signature Handler
Implements stateful reasoning preservation for function calling
"""

import logging
from typing import Any, Callable, Dict, Optional

import vertexai
from vertexai.generative_models import Content, GenerativeModel, Part, Tool

logger = logging.getLogger(__name__)


class ThoughtSignatureHandler:
    """
    Manages Gemini 3.0 Thought Signatures for stateful reasoning.

    Critical for Gemini 3.0: When the model invokes a function, it generates
    a 'thoughtSignature' representing the reasoning path. This MUST be preserved
    and returned in the follow-up call, or the model loses cognitive context.

    Reference: Migration Guide Section 3.2
    """

    def __init__(self, model: GenerativeModel, tools: list[Callable]):
        """
        Initialize handler with model and available tools.

        Args:
            model: GenerativeModel instance configured for Gemini 3.0
            tools: List of callable functions the model can invoke
        """
        self.model = model
        self.tools = {tool.__name__: tool for tool in tools}
        self.chat_session = None
        self.last_thought_signature = None

    def start_session(self) -> None:
        """Initialize a new chat session."""
        self.chat_session = self.model.start_chat()
        self.last_thought_signature = None
        logger.info("New reasoning session started")

    def execute_reasoning_turn(self, user_prompt: str) -> str:
        """
        Execute a single reasoning turn with proper thought signature handling.

        This implements the "Bare Metal" pattern from the migration guide,
        ensuring thought signatures are captured and propagated correctly.

        Args:
            user_prompt: User's input message

        Returns:
            Model's final text response

        Raises:
            RuntimeError: If session not started or function execution fails
        """
        if not self.chat_session:
            raise RuntimeError("Session not started. Call start_session() first.")

        # Step 1: Send initial message
        logger.debug(f"Sending user prompt: {user_prompt[:100]}...")
        response = self.chat_session.send_message(user_prompt)

        # Step 2: Check for function calls
        max_iterations = 10  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            try:
                # Get the first candidate's content parts
                candidate = response.candidates[0]
                parts = candidate.content.parts

                # Check if there's a function call
                has_function_call = False
                for part in parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_call = True
                        function_name = part.function_call.name
                        function_args = dict(part.function_call.args)

                        # CRITICAL: Extract thought signature
                        thought_signature = getattr(part, 'thought_signature', None)
                        if thought_signature:
                            self.last_thought_signature = thought_signature
                            logger.debug(
                                f"Captured thought signature: {str(thought_signature)[:50]}..."
                            )

                        # Step 3: Execute the function
                        logger.info(f"Executing function: {function_name} with args: {function_args}")
                        tool_result = self._execute_tool(function_name, function_args)

                        # Step 4: Send function response back
                        # The SDK handles thought signature propagation via session history
                        response_part = Part.from_function_response(
                            name=function_name,
                            response={"result": tool_result}
                        )

                        # Send the function result back to the model
                        response = self.chat_session.send_message(response_part)
                        break

                if not has_function_call:
                    # No function call, return the text response
                    return response.text

                iteration += 1

            except IndexError:
                logger.error("Response has no candidates")
                return "Erro: Resposta vazia do modelo."
            except Exception as e:
                logger.error(f"Error in reasoning turn: {str(e)}")
                raise

        if iteration >= max_iterations:
            logger.warning("Max reasoning iterations reached")
            return response.text if response else "Erro: Limite de iterações atingido."

        return response.text

    def _execute_tool(self, function_name: str, args: Dict[str, Any]) -> Any:
        """
        Execute a tool function and return its result.

        Args:
            function_name: Name of the function to execute
            args: Arguments to pass to the function

        Returns:
            Function execution result

        Raises:
            ValueError: If function not found
        """
        if function_name not in self.tools:
            logger.error(f"Function not found: {function_name}")
            return {"error": f"Function '{function_name}' not found"}

        try:
            tool_func = self.tools[function_name]
            result = tool_func(**args)
            logger.info(f"Tool '{function_name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {"error": f"Tool execution failed: {str(e)}"}

    def get_conversation_history(self) -> list[Content]:
        """
        Get the full conversation history including thought signatures.

        Returns:
            List of Content objects with full reasoning chain
        """
        if not self.chat_session:
            return []
        return self.chat_session.history


class ReasoningOrchestrator:
    """
    High-level orchestrator for complex multi-step reasoning tasks.

    Implements the recommended architecture for parecer processing:
    1. Validate inputs
    2. Gather context (OneTrust, CMDB)
    3. Analyze with deep reasoning
    4. Generate structured output
    """

    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        thinking_level: str = "high"
    ):
        """
        Initialize orchestrator.

        Args:
            project_id: Google Cloud project ID
            location: Vertex AI region
            thinking_level: "low" for fast responses, "high" for deep reasoning
        """
        vertexai.init(project=project_id, location=location)

        # Configure model with optimal settings
        self.model = GenerativeModel(
            "gemini-3.0-pro-001",
            generation_config={
                "thinking_level": thinking_level,
                "temperature": 1.0,  # Use default for reasoning
            }
        )

        self.thinking_level = thinking_level
        logger.info(f"Reasoning orchestrator initialized (thinking_level={thinking_level})")

    def should_use_high_reasoning(self, task_complexity: int) -> bool:
        """
        Decide whether to use high reasoning level based on task complexity.

        Implements the Tiered Architecture pattern from migration guide.

        Args:
            task_complexity: Score from 1-10

        Returns:
            True if high reasoning should be used
        """
        return task_complexity >= 5

    def execute_with_adaptive_reasoning(
        self,
        prompt: str,
        complexity_score: int
    ) -> str:
        """
        Execute with adaptive reasoning level.

        Args:
            prompt: User prompt
            complexity_score: Task complexity (1-10)

        Returns:
            Model response
        """
        should_think_deep = self.should_use_high_reasoning(complexity_score)

        if should_think_deep and self.thinking_level == "low":
            logger.warning(
                f"High complexity task (score={complexity_score}) but model "
                f"configured with thinking_level=low. Consider reconfiguring."
            )

        logger.info(
            f"Executing with thinking_level={self.thinking_level}, "
            f"complexity={complexity_score}"
        )

        response = self.model.generate_content(prompt)
        return response.text


# Example usage for the ANS agent
def create_ans_reasoning_handler(tools: list[Callable]) -> ThoughtSignatureHandler:
    """
    Create a reasoning handler for the ANS parecer agent.

    Args:
        tools: List of tool functions (integrar_onetrust, consultar_cmdb, etc.)

    Returns:
        Configured ThoughtSignatureHandler
    """
    import os
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'gft-bu-gcp')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')

    vertexai.init(project=project_id, location=location)

    model = GenerativeModel(
        "gemini-3-pro-preview",
        generation_config={
            "thinking_level": "high",  # Parecer analysis requires deep reasoning
            "temperature": 1.0,
        }
    )

    handler = ThoughtSignatureHandler(model, tools)
    logger.info("ANS Reasoning Handler created")

    return handler

