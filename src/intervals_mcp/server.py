"""
Intervals.icu MCP Server.

Provides access to intervals.icu training data, performance analytics,
and activity information through the Model Context Protocol.
"""

import os
import asyncio
import json
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from .utils.intervals_client import IntervalsClient
from .models.intervals_models import (
    Activity, ActivitySummary, Athlete, Wellness, Event,
    PerformanceAnalysis, ActivitySearchResult
)

load_dotenv()

app = Server("intervals-mcp-server")

@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available intervals.icu resources."""
    return [
        Resource(
            uri="intervals://activities",
            name="Recent Activities",
            description="User's recent intervals.icu activities and workouts",
            mimeType="application/json",
        ),
        Resource(
            uri="intervals://athlete",
            name="Athlete Profile", 
            description="User's intervals.icu athlete profile and settings",
            mimeType="application/json",
        ),
        Resource(
            uri="intervals://performance",
            name="Performance Analysis",
            description="Power curves, heart rate analysis, and performance metrics",
            mimeType="application/json",
        ),
        Resource(
            uri="intervals://wellness",
            name="Wellness Data",
            description="Sleep, HRV, and wellness tracking data",
            mimeType="application/json",
        ),
        Resource(
            uri="intervals://calendar",
            name="Training Calendar",
            description="Planned workouts, races, and training events",
            mimeType="application/json",
        ),
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific intervals.icu resource."""
    athlete_id = os.getenv("INTERVALS_ATHLETE_ID")
    if not athlete_id:
        raise ValueError("INTERVALS_ATHLETE_ID environment variable is required")
    
    async with IntervalsClient() as client:
        if uri == "intervals://activities":
            activities = await client.get_activities(athlete_id, limit=20)
            return f"Recent Activities:\n{json.dumps([activity.dict() for activity in activities], default=str, indent=2)}"
            
        elif uri == "intervals://athlete":
            athlete = await client.get_athlete(athlete_id)
            return f"Athlete Profile:\n{json.dumps(athlete.dict(), default=str, indent=2)}"
            
        elif uri == "intervals://performance":
            analysis = await client.get_performance_analysis(athlete_id)
            return f"Performance Analysis:\n{json.dumps(analysis.dict(), default=str, indent=2)}"
            
        elif uri == "intervals://wellness":
            from datetime import date, timedelta
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            try:
                wellness_data = await client.get_wellness_range(athlete_id, start_date, end_date)
                return f"Wellness Data (Last 30 Days):\n{json.dumps([w.dict() for w in wellness_data], default=str, indent=2)}"
            except Exception as e:
                return f"Wellness Data: No data available or error: {str(e)}"
                
        elif uri == "intervals://calendar":
            from datetime import date, timedelta
            start_date = date.today() - timedelta(days=7)
            end_date = date.today() + timedelta(days=14)
            try:
                events = await client.get_events(athlete_id, start_date, end_date)
                return f"Training Calendar:\n{json.dumps([event.dict() for event in events], default=str, indent=2)}"
            except Exception as e:
                return f"Training Calendar: No events or error: {str(e)}"
        else:
            raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available intervals.icu tools."""
    return [
        Tool(
            name="get_activities",
            description="Get recent activities with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of activities to retrieve (1-100)",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 20
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "Filter by activity type (Ride, Run, Swim, etc.)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string", 
                        "description": "End date in YYYY-MM-DD format"
                    }
                }
            }
        ),
        Tool(
            name="get_activity_details",
            description="Get detailed information about a specific activity including intervals",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "The intervals.icu activity ID"
                    },
                    "include_intervals": {
                        "type": "boolean",
                        "description": "Include detailed interval data",
                        "default": False
                    }
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="get_activity_streams",
            description="Get detailed time-series data for an activity (power, heart rate, GPS, etc.)",
            inputSchema={
                "type": "object", 
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "The intervals.icu activity ID"
                    }
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="search_activities",
            description="Search activities by text query, date range, or type",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text search query"
                    },
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
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="get_power_curve",
            description="Get athlete's power curve analysis showing peak power at different durations",
            inputSchema={
                "type": "object",
                "properties": {
                    "sport": {
                        "type": "string",
                        "description": "Filter by sport (Ride, Run, etc.)"
                    }
                }
            }
        ),
        Tool(
            name="get_activity_power_curve",
            description="Get power curve for a specific activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "The intervals.icu activity ID"
                    }
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="get_performance_analysis",
            description="Get comprehensive performance analysis including power, HR, and pace curves",
            inputSchema={
                "type": "object",
                "properties": {
                    "sport": {
                        "type": "string", 
                        "description": "Filter by sport (Ride, Run, etc.)"
                    },
                    "activity_id": {
                        "type": "string",
                        "description": "Include analysis for specific activity"
                    }
                }
            }
        ),
        Tool(
            name="get_best_efforts",
            description="Get best effort segments for an activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "The intervals.icu activity ID"
                    }
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="get_wellness_data",
            description="Get wellness data (sleep, HRV, stress, etc.) for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (defaults to 30 days ago)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (defaults to today)"
                    },
                    "date": {
                        "type": "string",
                        "description": "Single date in YYYY-MM-DD format (alternative to range)"
                    }
                }
            }
        ),
        Tool(
            name="get_training_calendar",
            description="Get planned workouts, races, and events from training calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (defaults to 7 days ago)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (defaults to 14 days from now)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by event category (WORKOUT, RACE, NOTE, etc.)"
                    }
                }
            }
        ),
        Tool(
            name="export_activities_csv",
            description="Export activities data as CSV format",
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
                    }
                }
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    athlete_id = os.getenv("INTERVALS_ATHLETE_ID")
    if not athlete_id:
        return [TextContent(type="text", text="Error: INTERVALS_ATHLETE_ID environment variable is required")]
    
    try:
        async with IntervalsClient() as client:
            if name == "get_activities":
                limit = arguments.get("limit", 20)
                activity_type = arguments.get("activity_type")
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                
                activities = await client.get_activities(
                    athlete_id, 
                    limit=limit,
                    start_date=start_date,
                    end_date=end_date,
                    activity_type=activity_type
                )
                
                result = {
                    "count": len(activities),
                    "activities": [activity.dict() for activity in activities]
                }
                return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
                
            elif name == "get_activity_details":
                activity_id = arguments.get("activity_id")
                include_intervals = arguments.get("include_intervals", False)
                
                if not activity_id:
                    return [TextContent(type="text", text="Error: activity_id is required")]
                    
                activity = await client.get_activity(activity_id, include_intervals)
                return [TextContent(type="text", text=json.dumps(activity.dict(), default=str, indent=2))]
                
            elif name == "get_activity_streams":
                activity_id = arguments.get("activity_id")
                
                if not activity_id:
                    return [TextContent(type="text", text="Error: activity_id is required")]
                    
                streams = await client.get_activity_streams(activity_id)
                result = {
                    "activity_id": activity_id,
                    "streams": [stream.dict() for stream in streams]
                }
                return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
                
            elif name == "search_activities":
                query = arguments.get("query")
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                activity_type = arguments.get("activity_type")
                limit = arguments.get("limit", 50)
                
                search_result = await client.search_activities(
                    athlete_id,
                    query=query,
                    start_date=start_date,
                    end_date=end_date,
                    activity_type=activity_type,
                    limit=limit
                )
                
                return [TextContent(type="text", text=json.dumps(search_result.dict(), default=str, indent=2))]
                
            elif name == "get_power_curve":
                sport = arguments.get("sport")
                
                power_curve = await client.get_power_curve(athlete_id, sport)
                return [TextContent(type="text", text=json.dumps(power_curve.dict(), default=str, indent=2))]
                
            elif name == "get_activity_power_curve":
                activity_id = arguments.get("activity_id")
                
                if not activity_id:
                    return [TextContent(type="text", text="Error: activity_id is required")]
                    
                power_curve = await client.get_activity_power_curve(activity_id)
                return [TextContent(type="text", text=json.dumps(power_curve.dict(), default=str, indent=2))]
                
            elif name == "get_performance_analysis":
                sport = arguments.get("sport")
                activity_id = arguments.get("activity_id")
                
                analysis = await client.get_performance_analysis(athlete_id, sport, activity_id)
                return [TextContent(type="text", text=json.dumps(analysis.dict(), default=str, indent=2))]
                
            elif name == "get_best_efforts":
                activity_id = arguments.get("activity_id")
                
                if not activity_id:
                    return [TextContent(type="text", text="Error: activity_id is required")]
                    
                best_efforts = await client.get_activity_best_efforts(activity_id)
                return [TextContent(type="text", text=json.dumps(best_efforts.dict(), default=str, indent=2))]
                
            elif name == "get_wellness_data":
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date") 
                single_date = arguments.get("date")
                
                if single_date:
                    wellness = await client.get_wellness(athlete_id, single_date)
                    return [TextContent(type="text", text=json.dumps(wellness.dict(), default=str, indent=2))]
                else:
                    if not start_date:
                        from datetime import date, timedelta
                        end_date = date.today()
                        start_date = end_date - timedelta(days=30)
                    if not end_date:
                        from datetime import date
                        end_date = date.today()
                        
                    wellness_data = await client.get_wellness_range(athlete_id, start_date, end_date)
                    result = {
                        "date_range": f"{start_date} to {end_date}",
                        "records": [w.dict() for w in wellness_data]
                    }
                    return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
                    
            elif name == "get_training_calendar":
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                category = arguments.get("category")
                
                if not start_date:
                    from datetime import date, timedelta
                    start_date = date.today() - timedelta(days=7)
                if not end_date:
                    from datetime import date, timedelta
                    end_date = date.today() + timedelta(days=14)
                    
                events = await client.get_events(athlete_id, start_date, end_date, category)
                result = {
                    "date_range": f"{start_date} to {end_date}",
                    "category": category or "all",
                    "events": [event.dict() for event in events]
                }
                return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
                
            elif name == "export_activities_csv":
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                
                csv_data = await client.export_activities_csv(athlete_id, start_date, end_date)
                return [TextContent(type="text", text=csv_data)]
                
            else:
                return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]
                
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="intervals-mcp-server",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(main())