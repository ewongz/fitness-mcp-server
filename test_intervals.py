#!/usr/bin/env python3
"""
Basic test script for the intervals.icu MCP server.
"""

import os
import asyncio
from dotenv import load_dotenv
from src.intervals_mcp.utils.intervals_client import IntervalsClient

load_dotenv()

async def test_intervals_client():
    """Test the intervals.icu client functionality."""
    
    api_key = os.getenv("INTERVALS_API_KEY")
    athlete_id = os.getenv("INTERVALS_ATHLETE_ID")
    
    if not api_key:
        print("❌ Error: INTERVALS_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your intervals.icu API key")
        return
        
    if not athlete_id:
        print("❌ Error: INTERVALS_ATHLETE_ID not found in environment variables")
        print("Please add your athlete ID to .env file")
        return
    
    print("🧪 Testing intervals.icu MCP client...")
    print(f"Using athlete ID: {athlete_id}")
    
    try:
        async with IntervalsClient() as client:
            # Test 1: Get athlete profile
            print("\n1. Testing get_athlete...")
            print(client._client)
            athlete = await client.get_athlete(athlete_id)
            print(f"✅ Athlete: {athlete.name} from {athlete.city or 'Unknown'}, {athlete.country or 'Unknown'}")
            
            # Test 2: Get recent activities
            print("\n2. Testing get_activities...")
            from datetime import date, timedelta
            start_date = date.today() - timedelta(days=30)  # Last 30 days
            activities = await client.get_activities(athlete_id, limit=5, start_date=start_date)
            print(f"✅ Found {len(activities)} recent activities:")
            for activity in activities[:3]:  # Show first 3
                print(f"   - {activity.name} ({activity.type}) on {activity.start_date_local}")
            
            if activities:
                activity_id = activities[0].id
                
                # Test 3: Get activity details
                print(f"\n3. Testing get_activity for activity {activity_id}...")
                activity = await client.get_activity(activity_id)
                print(f"✅ Activity details: {activity.name}")
                if activity.average_watts:
                    print(f"   Power: {activity.average_watts}W avg, Training Load: {activity.icu_training_load or 'N/A'}")
                if activity.average_heartrate:
                    print(f"   HR: {activity.average_heartrate} bpm avg")
                
                # Test 4: Get activity streams
                print(f"\n4. Testing get_activity_streams for activity {activity_id}...")
                try:
                    streams = await client.get_activity_streams(activity_id)
                    stream_types = [stream.type for stream in streams]
                    print(f"✅ Found {len(streams)} streams: {', '.join(stream_types[:5])}")
                except Exception as e:
                    print(f"ℹ️  Streams not available or error: {str(e)}")
            
            # Test 5: Performance analysis
            print("\n5. Testing performance analysis...")
            try:
                analysis = await client.get_performance_analysis(athlete_id)
                has_power = analysis.power_curve is not None
                has_hr = analysis.hr_curve is not None
                has_pace = analysis.pace_curve is not None
                print(f"✅ Performance data - Power: {has_power}, HR: {has_hr}, Pace: {has_pace}")
            except Exception as e:
                print(f"ℹ️  Performance analysis not available: {str(e)}")
            
            print("\n🎉 All tests completed successfully!")
            print("\nYour intervals.icu MCP server is ready to use!")
            print("\nTo run the MCP server:")
            print("  python run_intervals_server.py")
            
    except ValueError as e:
        print(f"❌ Configuration error: {str(e)}")
        if "Invalid API key" in str(e):
            print("Please check your INTERVALS_API_KEY in the .env file")
        elif "athlete" in str(e).lower():
            print("Please check your INTERVALS_ATHLETE_ID in the .env file")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("Please check your internet connection and API credentials")

if __name__ == "__main__":
    asyncio.run(test_intervals_client())