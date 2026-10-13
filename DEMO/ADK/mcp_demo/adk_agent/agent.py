
# ============================================================
# PART 2
# ADK MULTI-AGENT WORKFLOW
#
# File: adk_agent/agent.py
# ============================================================
"""
Note: You don't actually start the MCP server separately.
ADK itself launches: python mcp_server.py as a subprocess.
"""

"""
------------------------------------------------
The Execution should conceptually be as follows
------------------------------------------------

User
 │
 ▼
CityInfoAgent
 │
 │ calls city_info
 ▼
MCP Client
 │
 │ MCP / stdio
 ▼
MCP Server
 │
 └── city_info()
       │
       ▼
CityInfoAgent
       │
       │ state["city_info"]
       ▼
WeatherAgent
       │
       │ calls get_weather
       ▼
MCP Server
       │
       └── get_weather()
              │
              ▼
       WeatherAgent
              │
              ▼
        Final Answer
"""

import os

from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from mcp import StdioServerParameters

import os

#--------------------------------------
# Set the path of the mcp server
MCP_SERVER_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "mcp_server.py",
    )
)

#--------------------------------------------
# Define the MCP Toolset
"""
McpToolset is the ADK-side bridge to an MCP server. 
It manages the MCP connection, discovers the MCP server's tools, 
wraps those tools as ADK tools, and routes tool calls back to the MCP server. 
The current ADK implementation explicitly describes McpToolset as connecting to an MCP server and retrieving MCP tools into ADK

Conceptually, the MCP client is the MCP client/session machinery inside McpToolset.
ADK's McpToolset internally manages an MCP session manager/client connection. 
The implementation creates MCP sessions, calls list_tools(), and creates McpTool wrappers around the discovered MCP tools.
"""
#--------------------------------------------

mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[MCP_SERVER_PATH],
        ),
        timeout=10,
    ),

    tool_filter=[
        "city_info",
        "get_weather",
    ],
)


#--------------------------------------------
# City-info Agent
#--------------------------------------------
city_info_agent = LlmAgent(
    name="CityInfoAgent",
    model="gemini-3.5-flash-lite",

    instruction="""
    You are a City Information Specialist.

    Use the MCP tool city_info to obtain
    information about the requested city.

    Save your summary for the next agent.
    """,

    tools=[mcp_tools],

    output_key="city_info",
)


#--------------------------------------------
# Weather Agent
#--------------------------------------------
weather_agent = LlmAgent(
    name="WeatherAgent",
    model="gemini-3.5-flash-lite",

    instruction="""
    You are a Weather Specialist.

    Use the MCP tool get_weather to obtain
    the weather for the requested city.

    You may use the previous agent's result:

    {city_info}

    Combine the information and produce
    the final answer.
    """,

    tools=[mcp_tools],
)

# Root Agent
root_agent = SequentialAgent(
    name="TravelInformationWorkflow",

    sub_agents=[
        city_info_agent,
        weather_agent,
    ],
)

# Example Usage:
# Use `adk web`` command to run the script
# Tell me about Venice
