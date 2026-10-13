=============================================================
MCP + ADK MULTI-AGENT EXAMPLE
=============================================================

Architecture:

                    MCP SERVER
              ┌────────────────────┐
              │  city_info_tool    │
              │  get_weather_tool  │
              └─────────┬──────────┘
                        │
                   MCP / stdio
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼

CityInfoAgent WeatherAgent
│ │
└──────── Shared State ─────┘
│
▼
Final Response

The example contains:

1. A custom MCP server exposing two tools:
   - city_info
   - get_weather

2. Two ADK agents:
   - CityInfoAgent
   - WeatherAgent

3. Both agents consume tools from the MCP server.

4. SequentialAgent controls execution.

5. CityInfoAgent stores its result in:
   state["city_info"]

6. WeatherAgent reads that result and produces
   the final response.

=============================================================
PROJECT STRUCTURE
=============================================================

mcp_adk_demo/
│
├── .env
│
├── mcp_server.py
│
└── adk_agent/
├── **init**.py
└── agent.py

=============================================================
INSTALL
=============================================================

pip install google-adk mcp python-dotenv

=============================================================
.env
=============================================================

GOOGLE_API_KEY=your_google_api_key

=============================================================
