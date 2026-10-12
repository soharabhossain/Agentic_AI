
#---------------------------------------------
# DEMO: Tool Callbacks with State Management
#---------------------------------------------

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
import yfinance as yf
from typing import Dict, Any, Optional

import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------
# Get Stock Price Tool
#------------------------------------------------------------------------
def get_stock_data(ticker: str, tool_context: ToolContext):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", 0)
    
    # Initialize tool_usage in state if it doesn't exist
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}
    
    return {
        "ticker": ticker,
        "price": price
    }
#------------------------------------------------------------------------
# Get Current Time Tool
#------------------------------------------------------------------------
def get_current_time(city: str, tool_context: ToolContext) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    # Initialize tool_usage in state if it doesn't exist
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}


    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

#------------------------------------------------------------------------

def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    # Initialize tool_usage if it doesn't exist
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}
    
    # Track tool usage count
    tool_usage = tool_context.state["tool_usage"]
    tool_name = tool.name
    tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    tool_context.state["tool_usage"] = tool_usage
    
    print(f"[LOG][Before Callback] Running tool: {tool_name} is being used {tool_usage[tool_name]} times")
    print(f"[LOG][Before Callback] Tool Context State Dict Keys: {tool_context.state.__dict__.keys()}\n")
    print(f"[LOG][Before Callback] Tool Context State _Value: {tool_context.state._value}\n")
    print(f"[LOG][Before Callback] Tool Context State _Delta: {tool_context.state._delta}\n")

    return None

def after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    print(f"[LOG][After Callback] Tool {tool.name} completed")
    print(f"[LOG][After Callback] Tool Dict Keys : {tool.__dict__.keys()}")
    print(f"[LOG][After Callback] ToolContext Dict Keys: {tool_context.__dict__.keys()}")
    print(f"[LOG][After Callback] ToolContext Invocation Context: {tool_context._invocation_context}")
    print(f"[LOG][After Callback] ToolContext State Dict Keys: {tool_context.state.__dict__.keys()}")
    print(f"[LOG][After Callback] ToolContext State _Value: {tool_context.state._value}")
    print(f"[LOG][After Callback] ToolContext State _Delta: {tool_context.state._delta}")

    return None

#------------------------------------------------------------------------
# Initialize state before creating the agent
# initial_state = {"tool_usage": {}}

callback_agent = Agent(
    name="callback_agent",
    model="gemini-2.0-flash",
    description="An agent with callbacks",
    instruction="""
    You are a helpful AI assistant. You have access to 2 tools.
     Use get_stock_data tool to check stock prices.
     Use get_current_time tool to check the current time in a city.
    You are an agent who keeps track of how many times tools have been used.
    """,
    tools=[get_stock_data, get_current_time],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

# Choose which agent to run
root_agent = callback_agent

