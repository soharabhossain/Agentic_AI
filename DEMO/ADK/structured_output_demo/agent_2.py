# ERROR running the code! Function call parameter parsing error!!!

# DEMO: Structured Output Agent
# pip install yfinance

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
import yfinance as yf
from google.adk.agents.invocation_context import InvocationContext

class StockAnalysis(BaseModel):
    ticker: str = Field(description="Stock symbol")
    recommendation: str = Field(description="Buy or Sell recommendation")

# Define a function to get stock data for our prompt
def get_stock_data_for_prompt(ctx: InvocationContext):
    ticker=ctx.session.state.get("ticker", "")
    if ticker == "":
      raise ValueError("Ticker symbol is required.")
    else:
      print(ticker)  
      stock = yf.Ticker(ticker)
      price = stock.info.get("currentPrice", 0)
      target_price = stock.info.get("targetMeanPrice", 0)
      return price, target_price

structured_agent = LlmAgent(
    name="structured_agent",
    model="gemini-2.0-flash",
    description="An agent with structured output",
    instruction="""
    You are a stock advisor. Analyze the stock ticker provided by the user.

    To get the stock data, you must call the `get_stock_data_for_prompt` tool.
    You must extract the stock ticker symbol from the user query and 
     update `state['ticker']` with the stock ticker symbol before calling the `get_stock_data_for_prompt` tool.

    For each ticker, look at the price and target price to make a decision.
    If target price > current price: recommend Buy
    Otherwise: recommend Sell
    Return Buy or Sell recommendation in JSON format.
    """,
    tools=[get_stock_data_for_prompt],
    output_schema=StockAnalysis,
    output_key="stock_analysis"
)

# This is where you would handle the user query.
# For example, to handle a query like "What should I do with AAPL stock?":
query = "What should I do with AAPL stock?"

# The agent's instruction, along with the tool definition,
# enables it to understand that when the user provides a ticker
# like 'AAPL', it should call the tool with that value.
# The user's query "What should I do with AAPL stock?" will trigger the tool call.

root_agent = structured_agent
