
from dotenv import load_dotenv
load_dotenv()

"""
# Iterative Refinement Pattern
Structure: Uses a LoopAgent containing one or more agents that work on a task over multiple iterations.
Goal: Progressively improve a result (e.g., code, text, plan) stored in the session state until a quality threshold is met or a maximum number of iterations is reached.
ADK Primitives Used:
Workflow: LoopAgent manages the repetition.
Communication: Shared Session State is essential for agents to read the previous iteration's output and save the refined version.
Termination: The loop typically ends based on max_iterations or a dedicated checking agent setting escalate=True in the Event Actions when the result is satisfactory.
"""

# Conceptual Code: Iterative Code Refinement
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

# Agent to generate/refine code based on state['current_code'] and state['requirements']
code_refiner = LlmAgent(
    name="CodeRefiner",
    instruction="Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    model="gemini-2.0-flash",
    output_key="current_code" # Overwrites previous code in state
)

# Agent to check if the code meets quality standards
# If the code is good, it outputs 'pass', else 'fail'
quality_checker = LlmAgent(
    name="QualityChecker",
    instruction="Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    model="gemini-2.0-flash",
    output_key="quality_status"
)

# Custom agent to check the status and escalate if 'pass'
class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("quality_status", "fail")
        should_stop = (status == "pass")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

refinement_loop = LoopAgent(
    name="CodeRefinementLoop",
    max_iterations=5,
    sub_agents=[code_refiner, quality_checker, CheckStatusAndEscalate(name="StopChecker")]
)

root_agent = refinement_loop

# Loop runs: Refiner -> Checker -> StopChecker
# State['current_code'] is updated each iteration.
# Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.