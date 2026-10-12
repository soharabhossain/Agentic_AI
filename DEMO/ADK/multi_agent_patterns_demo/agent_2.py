
from dotenv import load_dotenv
load_dotenv()

# Test Run
# 2+3=5

"""
# Sequential Pipeline Pattern
Structure: A SequentialAgent contains sub_agents executed in a fixed order.
Goal: Implement a multi-step process where the output of one step feeds into the next.
ADK Primitives Used:
Workflow: SequentialAgent defines the order.
Communication: Primarily uses Shared Session State. 
Earlier agents write results (often via output_key), later agents read those results from context.state.
"""
# Conceptual Code: Sequential Data Pipeline
from google.adk.agents import SequentialAgent, LlmAgent

validator = LlmAgent(
  name="ValidateInput", 
  instruction="Validate the input.", 
  model="gemini-2.0-flash",
  output_key="validation_status")

processor = LlmAgent(
  name="ProcessData", 
  instruction="Process data if {validation_status} is 'valid'.", 
  model="gemini-2.0-flash",
  output_key="result")

reporter = LlmAgent(
  name="ReportResult",
  instruction="Report the result from {result}.",
  model="gemini-2.0-flash",

  )

data_pipeline = SequentialAgent(
    name="DataPipeline",
    sub_agents=[validator, processor, reporter]
)

root_agent = data_pipeline

# validator runs -> saves to state['validation_status']
# processor runs -> reads state['validation_status'], saves to state['result']
# reporter runs -> reads state['result']
