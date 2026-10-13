# ============================================================
# PART 1
# CUSTOM MCP SERVER
#
# File: mcp_server.py
# ============================================================

from mcp.server import MCPServer

mcp = MCPServer("CityInformationServer")


@mcp.tool()
def city_info(city: str) -> str:
    """Return basic information about a city."""

    database = {
        "venice": (
            "Venice is a city in northeastern Italy, "
            "famous for its canals, gondolas and historic architecture."
        ),
        "paris": (
            "Paris is the capital of France, famous for "
            "the Eiffel Tower, Louvre and its cultural heritage."
        ),
    }

    return database.get(
        city.lower(),
        f"No information available for {city}."
    )


@mcp.tool()
def get_weather(city: str) -> str:
    """Return weather information for a city."""

    weather = {
        "venice": "22°C, partly cloudy, humidity 68%.",
        "paris": "18°C, cloudy, humidity 72%.",
    }

    return weather.get(
        city.lower(),
        f"Weather information unavailable for {city}."
    )


if __name__ == "__main__":
    mcp.run()