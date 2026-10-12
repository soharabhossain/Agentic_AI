
# Test Run
# carbon footprint

from dotenv import load_dotenv
load_dotenv()

"""
# Hierarchical Task Decomposition
Structure: A multi-level tree of agents where higher-level agents break down complex goals and delegate sub-tasks to lower-level agents.
Goal: Solve complex problems by recursively breaking them down into simpler, executable steps.
ADK Primitives Used:
Hierarchy: Multi-level parent_agent/sub_agents structure.
Interaction: Primarily LLM-Driven Delegation or Explicit Invocation (AgentTool) 
used by parent agents to assign tasks to subagents. 
Results are returned up the hierarchy (via tool responses or state).
"""
# Conceptual Code: Hierarchical Research Task
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search


# Low-level tool-like agents
web_searcher = LlmAgent(name="WebSearch", 
description="Performs web searches for facts.",
model="gemini-2.0-flash",
tools=[google_search])

summarizer = LlmAgent(name="Summarizer", 
description="Summarizes text.",
model="gemini-2.0-flash",
)

# Mid-level agent combining tools
research_assistant = LlmAgent(
    name="ResearchAssistant",
    model="gemini-2.0-flash",
    description="Finds and summarizes information on a topic.",
    # tools=[agent_tool.AgentTool(agent=web_searcher), agent_tool.AgentTool(agent=summarizer)]
    tools=[AgentTool(agent=web_searcher), AgentTool(agent=summarizer)]

)

# High-level agent delegating research
report_writer = LlmAgent(
    name="ReportWriter",
    model="gemini-2.0-flash",
    instruction="Write a report on topic X. Use the ResearchAssistant to gather information.",
    tools=[AgentTool(agent=research_assistant)]
    # Alternatively, could use LLM Transfer if research_assistant is a sub_agent
)

root_agent = report_writer

# User interacts with ReportWriter.
# ReportWriter calls ResearchAssistant tool.
# ResearchAssistant calls WebSearch and Summarizer tools.
# Results flow back up.
