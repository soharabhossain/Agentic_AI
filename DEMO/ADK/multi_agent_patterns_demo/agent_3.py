# Test Run
# Venice


"""
# Parallel Fan-Out/Gather Pattern
Structure: A ParallelAgent runs multiple sub_agents concurrently, often followed by a later agent (in a SequentialAgent) that aggregates results.
Goal: Execute independent tasks simultaneously to reduce latency, then combine their outputs.
ADK Primitives Used:
Workflow: ParallelAgent for concurrent execution (Fan-Out). 
Often nested within a SequentialAgent to handle the subsequent aggregation step (Gather).
Communication: Sub-agents write results to distinct keys in Shared Session State. 
The subsequent "Gather" agent reads multiple state keys.
"""

from dotenv import load_dotenv
load_dotenv()

# Conceptual Code: Parallel Information Gathering
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from google.adk.tools import google_search

fetch_api1 = LlmAgent(name="CityInfoFetcher", 
                      instruction="Fetch interesting information about a city and provide a small paragraph.", 
                      model="gemini-2.0-flash",
                      tools=[google_search],
                      output_key="api1_data")

fetch_api2 = LlmAgent(name="CityWeatherFetcher", 
                      instruction="Fetch current weather information about a city and provide a small paragraph.", 
                      model="gemini-2.0-flash",
                      tools=[google_search],
                      output_key="api2_data")

gather_concurrently = ParallelAgent(
    name="ConcurrentFetch",
    sub_agents=[fetch_api1, fetch_api2]
)

synthesizer = LlmAgent(
    name="Synthesizer",
    instruction="Combine results from {api1_data} and {api2_data}.",
    model="gemini-2.0-flash",

)

overall_workflow = SequentialAgent(
    name="FetchAndSynthesize",
    sub_agents=[gather_concurrently, synthesizer] # Run parallel fetch, then synthesize
)
root_agent = overall_workflow

# fetch_api1 and fetch_api2 run concurrently, saving to state.
# synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].



