
from dotenv import load_dotenv
load_dotenv()

"""
# Review/Critique Pattern (Generator-Critic)
Structure: Typically involves two agents within a SequentialAgent: a Generator and a Critic/Reviewer.
Goal: Improve the quality or validity of generated output by having a dedicated agent review it.
ADK Primitives Used:
Workflow: SequentialAgent ensures generation happens before review.
Communication: Shared Session State (Generator uses output_key to save output; Reviewer reads that state key). 
The Reviewer might save its feedback to another state key for subsequent steps.
"""

# Conceptual Code: Generator-Critic
from google.adk.agents import SequentialAgent, LlmAgent

generator = LlmAgent(
    name="DraftWriter",
    instruction="Write a short paragraph about subject X.",
    model="gemini-2.0-flash",
    output_key="draft_text"
)

reviewer = LlmAgent(
    name="FactChecker",
    instruction="Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    model="gemini-2.0-flash",
    output_key="review_status"
)

# Optional: Further steps based on review_status

review_pipeline = SequentialAgent(
    name="WriteAndReview",
    sub_agents=[generator, reviewer]
)

root_agent = review_pipeline

# generator runs -> saves draft to state['draft_text']
# reviewer runs -> reads state['draft_text'], saves status to state['review_status']

