
# pip install langchain

"""
This agent aims to test the Langchain tool with Langchain's StructuredTool
"""
from google.adk.agents.llm_agent import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain.tools import tool
from langchain_core.tools.structured import StructuredTool
from pydantic import BaseModel


# add is a regular async function
async def add(x, y) -> int:
  """tool to be used for adding two numbers """ #<= docstring must be present for StructuredTool to work properly
  return x + y

# a tool
@tool
def minus(x, y) -> int:
  """tool to be used for subtract one number from another """ #<= docstring must be present for StructuredTool to work properly
  return x - y
#----------------------------------------
# Schema for the tool
class AddSchema(BaseModel):
  x: int
  y: int

class MinusSchema(BaseModel):
  x: int
  y: int
#----------------------------------------

# Create Langchain StructuredTool instances
# Convert a regular function to a Langchain StructuredTool
langchain_add_tool = StructuredTool.from_function(
    add,
    name="add",
    description="Adds two numbers",
    args_schema=AddSchema,
)
#----------------------------------------

# Create the Agent
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="test_app",
    description="A helpful assistant for user questions.",
    instruction=(
        "You are a helpful assistant for user questions, you have access to a"
        " tool that adds two numbers."
    ),
    tools=[
        LangchainTool(tool=langchain_add_tool),
        LangchainTool(tool=minus),
    ],
)