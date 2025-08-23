import os
import asyncio
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from .utils.strava_client import StravaClient
from .models.strava_models import Activity, Athlete

load_dotenv()

app = Server("strava-mcp-server")

@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available Strava resources."""
    return [
        Resource(
            uri="strava://activities",
            name="Recent Activities",
            description="User's recent Strava activities",
            mimeType="application/json",
        ),
        Resource(
            uri="strava://athlete",
            name="Athlete Profile",
            description="User's Strava athlete profile",
            mimeType="application/json",
        ),
        Resource(
            uri="strava://stats",
            name="Athlete Stats",
            description="User's all-time Strava statistics",
            mimeType="application/json",
        ),
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific Strava resource."""
    client = StravaClient()
    
    if uri == "strava://activities":
        activities = await client.get_recent_activities(limit=30)
        return f"Recent Activities:\n{activities}"
    elif uri == "strava://athlete":
        athlete = await client.get_athlete()
        return f"Athlete Profile:\n{athlete}"
    elif uri == "strava://stats":
        stats = await client.get_athlete_stats()
        return f"Athlete Statistics:\n{stats}"
    else:
        raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available Strava tools."""
    return [
        Tool(
            name="get_activities",
            description="Get recent Strava activities with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of activities to retrieve (1-200)",
                        "minimum": 1,
                        "maximum": 200,
                        "default": 30
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "Filter by activity type (Run, Ride, Swim, etc.)",
                        "enum": ["Run", "Ride", "Swim", "Walk", "Hike", "AlpineSki", "BackcountrySki", "Canoeing", "Crossfit"]
                    }
                }
            }
        ),
        Tool(
            name="get_activity_details",
            description="Get detailed information about a specific activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "The Strava activity ID"
                    }
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="get_athlete_stats",
            description="Get athlete's all-time statistics",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="search_activities",
            description="Search activities by date range or other criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "Filter by activity type"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    client = StravaClient()
    
    try:
        if name == "get_activities":
            limit = arguments.get("limit", 30)
            activity_type = arguments.get("activity_type")
            activities = await client.get_recent_activities(limit=limit, activity_type=activity_type)
            return [TextContent(type="text", text=str(activities))]
            
        elif name == "get_activity_details":
            activity_id = arguments.get("activity_id")
            if not activity_id:
                raise ValueError("activity_id is required")
            activity = await client.get_activity_details(activity_id)
            return [TextContent(type="text", text=str(activity))]
            
        elif name == "get_athlete_stats":
            stats = await client.get_athlete_stats()
            return [TextContent(type="text", text=str(stats))]
            
        elif name == "search_activities":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            activity_type = arguments.get("activity_type")
            activities = await client.search_activities(
                start_date=start_date,
                end_date=end_date, 
                activity_type=activity_type
            )
            return [TextContent(type="text", text=str(activities))]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="strava-mcp-server",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(main())