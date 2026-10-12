
from dotenv import load_dotenv
load_dotenv()

"""
# LoopAgent: Executes its sub_agents sequentially in a loop.
Termination: The loop stops if the optional max_iterations is reached, or if any sub-agent returns an Event with escalate=True in it's Event Actions.
Context & State: Passes the same InvocationContext in each iteration, allowing state changes (e.g., counters, flags) to persist across loops.
"""
# Conceptual Example: Loop with Condition
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator


# Custom Agent to check state
class CheckCondition(BaseAgent): 
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("status", "pending")
        is_done = (status == "completed")
        yield Event(author=self.name, actions=EventActions(escalate=is_done)) # Escalate if done

# LlmAgent that might update state
process_step = LlmAgent(name="ProcessingStep",
                        instruction="Perform a processing step and update status to 'completed' when done.",
                        model="gemini-2.0-flash",
                        ) # Agent that might update state['status']

# LoopAgent that runs process_step and CheckCondition
poller = LoopAgent(
    name="StatusPoller",
    max_iterations=10,
    sub_agents=[process_step, CheckCondition(name="Checker")]
)

root_agent = poller


# When poller runs, it executes process_step then Checker repeatedly
# until Checker escalates (state['status'] == 'completed') or 10 iterations pass.
