
from dotenv import load_dotenv
load_dotenv()

"""
# Human-in-the-Loop Pattern
Structure: Integrates human intervention points within an agent workflow.
Goal: Allow for human oversight, approval, correction, or tasks that AI cannot perform.
ADK Primitives Used (Conceptual):
Interaction: Can be implemented using a custom Tool that pauses execution and sends a request to an external system (e.g., a UI, ticketing system) waiting for human input. 
The tool then returns the human's response to the agent.
Workflow: Could use LLM-Driven Delegation (transfer_to_agent) targeting a conceptual "Human Agent" that triggers the external workflow, or use the custom tool within an LlmAgent.
State/Callbacks: State can hold task details for the human; 
callbacks can manage the interaction flow.

Note: ADK doesn't have a built-in "Human Agent" type, so this requires custom integration.
"""

# Conceptual Code: Using a Tool for Human Approval
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool


# Custom tool to simulate human approval process
def external_approval_tool():
    human_input = input("Requesting human approval. Do you approve or reject? (Type 'approved' or 'rejected'):")
    return human_input

# --- Assume external_approval_tool exists ---
# This tool would:
# 1. Take details (e.g., request_id, amount, reason).
# 2. Send these details to a human review system (e.g., via API).
# 3. Poll or wait for the human response (approved/rejected).
# 4. Return the human's decision.
# async def external_approval_tool(amount: float, reason: str) -> str: ...
approval_tool = FunctionTool(func=external_approval_tool)

# Agent that prepares the request
prepare_request = LlmAgent(
    name="PrepareApproval",
    instruction="""Prepare the approval request details based on user input. Store amount and reason in state.
    Likely set the state['approval_amount'] with the approval amount and mention a reason in state['approval_reason']""",
    model="gemini-2.0-flash",
    # output_key="approval_details"  # Conceptual; could set multiple state keys
)

# Agent that calls the human approval tool
request_approval = LlmAgent(
    name="RequestHumanApproval",
    instruction="Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].",
    model="gemini-2.0-flash",
    tools=[approval_tool],
    output_key="human_decision"
)

# Agent that proceeds based on human decision
process_decision = LlmAgent(
    name="ProcessDecision",
    model="gemini-2.0-flash",
    instruction="Check {human_decision}. If 'approved', proceed. If 'rejected', inform user."
)

approval_workflow = SequentialAgent(
    name="HumanApprovalWorkflow",
    sub_agents=[prepare_request, request_approval, process_decision]
)

root_agent = approval_workflow

# prepare_request runs -> sets state['approval_amount'], state['approval_reason']
# request_approval runs -> calls external_approval_tool, sets state['human_decision']
# process_decision runs -> reads state['human_decision'], takes action accordingly

#--------------------------------------------------------------------------------------
# Test Run
# Submiting a bill of Rs. 5000 towards transportation cost for business travel to attend an outreach program
# approved

# submissing a bill of Rs 100 for having fun
# rejected
