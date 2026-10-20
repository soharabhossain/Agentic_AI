
# A2A/a2a_fact_checker/root_agent/agent.py

# Consumer/Root agent
from dotenv import load_dotenv
load_dotenv()

from google.adk import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)


fact_checker = RemoteA2aAgent(
    name="fact_checker",
    description="Remote agent that provides factual information.",
    agent_card=(
        f"http://localhost:8001"
        f"{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
    use_legacy=False,
)


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash-lite",
    description="Root agent that delegates factual queries.",
    instruction="""
You are the root orchestration agent.

When the user asks for factual information or interesting
facts, delegate the request to the fact_checker agent.

Present the response received from the fact_checker clearly
to the user.
""",
    sub_agents=[fact_checker],
)