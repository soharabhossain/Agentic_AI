# A2A/a2a_fact_checker/fact_checker_remote/agent.py

import os
from dotenv import load_dotenv
load_dotenv()

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import google_search


root_agent = Agent(
    name="facts_agent",
    model="gemini-2.5-flash-lite",
    description="Agent to give interesting facts.",
    instruction=(
        "You are a helpful agent who can provide interesting facts. "
        "Use Google Search when necessary."
    ),
    tools=[google_search],
)

a2a_app = to_a2a(
    root_agent,
    port=int(os.getenv("PORT", "8001")),
)