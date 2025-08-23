import os
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from ..models.strava_models import Activity, Athlete, AthleteStats


class StravaClient:
    """Client for interacting with Strava API."""
    
    BASE_URL = "https://www.strava.com/api/v3"
    
    def __init__(self):
        self.access_token = os.getenv("STRAVA_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("STRAVA_ACCESS_TOKEN environment variable is required")
        
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            timeout=30.0
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an authenticated request to Strava API."""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = await self.client.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid or expired Strava access token")
            elif e.response.status_code == 403:
                raise ValueError("Insufficient permissions to access this resource")
            elif e.response.status_code == 429:
                raise ValueError("Strava API rate limit exceeded")
            else:
                raise ValueError(f"Strava API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise ValueError(f"Network error when connecting to Strava API: {str(e)}")
    
    async def get_athlete(self) -> str:
        """Get authenticated athlete's profile."""
        data = await self._make_request("GET", "/athlete")
        
        athlete = Athlete(
            id=data["id"],
            username=data.get("username"),
            resource_state=data["resource_state"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            bio=data.get("bio"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            sex=data.get("sex"),
            premium=data.get("premium", False),
            summit=data.get("summit", False),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            badge_type_id=data.get("badge_type_id"),
            weight=data.get("weight"),
            profile_medium=data.get("profile_medium"),
            profile=data.get("profile"),
            friend=data.get("friend"),
            follower=data.get("follower"),
        )
        
        return str(athlete)
    
    async def get_recent_activities(self, limit: int = 30, activity_type: Optional[str] = None) -> str:
        """Get recent activities for the authenticated athlete."""
        params = {"per_page": min(limit, 200), "page": 1}
        
        data = await self._make_request("GET", "/athlete/activities", params=params)
        
        activities = []
        for item in data:
            if activity_type and item["type"] != activity_type:
                continue
                
            activity = Activity(
                resource_state=item["resource_state"],
                athlete=item["athlete"],
                name=item["name"],
                distance=item["distance"],
                moving_time=item["moving_time"],
                elapsed_time=item["elapsed_time"],
                total_elevation_gain=item["total_elevation_gain"],
                type=item["type"],
                sport_type=item.get("sport_type", item["type"]),
                workout_type=item.get("workout_type"),
                id=item["id"],
                start_date=item["start_date"],
                start_date_local=item["start_date_local"],
                timezone=item["timezone"],
                utc_offset=item["utc_offset"],
                location_city=item.get("location_city"),
                location_state=item.get("location_state"),
                location_country=item.get("location_country"),
                achievement_count=item["achievement_count"],
                kudos_count=item["kudos_count"],
                comment_count=item["comment_count"],
                athlete_count=item["athlete_count"],
                photo_count=item["photo_count"],
                map=item.get("map"),
                trainer=item["trainer"],
                commute=item["commute"],
                manual=item["manual"],
                private=item["private"],
                visibility=item["visibility"],
                flagged=item["flagged"],
                gear_id=item.get("gear_id"),
                start_latlng=item.get("start_latlng"),
                end_latlng=item.get("end_latlng"),
                average_speed=item["average_speed"],
                max_speed=item["max_speed"],
                average_cadence=item.get("average_cadence"),
                average_watts=item.get("average_watts"),
                weighted_average_watts=item.get("weighted_average_watts"),
                kilojoules=item.get("kilojoules"),
                device_watts=item.get("device_watts", False),
                has_heartrate=item["has_heartrate"],
                average_heartrate=item.get("average_heartrate"),
                max_heartrate=item.get("max_heartrate"),
                heartrate_opt_out=item.get("heartrate_opt_out", False),
                display_hide_heartrate_option=item.get("display_hide_heartrate_option", False),
                elev_high=item.get("elev_high"),
                elev_low=item.get("elev_low"),
                upload_id=item.get("upload_id"),
                upload_id_str=item.get("upload_id_str"),
                external_id=item.get("external_id"),
                from_accepted_tag=item.get("from_accepted_tag", False),
                pr_count=item["pr_count"],
                total_photo_count=item["total_photo_count"],
                has_kudoed=item["has_kudoed"],
            )
            activities.append(activity)
        
        if not activities:
            return "No activities found."
        
        result = f"Found {len(activities)} activities:\n\n"
        for i, activity in enumerate(activities, 1):
            result += f"{i}. {str(activity)}\n\n"
        
        return result
    
    async def get_activity_details(self, activity_id: str) -> str:
        """Get detailed information about a specific activity."""
        data = await self._make_request("GET", f"/activities/{activity_id}")
        
        activity = Activity(
            resource_state=data["resource_state"],
            athlete=data["athlete"],
            name=data["name"],
            distance=data["distance"],
            moving_time=data["moving_time"],
            elapsed_time=data["elapsed_time"],
            total_elevation_gain=data["total_elevation_gain"],
            type=data["type"],
            sport_type=data.get("sport_type", data["type"]),
            workout_type=data.get("workout_type"),
            id=data["id"],
            start_date=data["start_date"],
            start_date_local=data["start_date_local"],
            timezone=data["timezone"],
            utc_offset=data["utc_offset"],
            location_city=data.get("location_city"),
            location_state=data.get("location_state"),
            location_country=data.get("location_country"),
            achievement_count=data["achievement_count"],
            kudos_count=data["kudos_count"],
            comment_count=data["comment_count"],
            athlete_count=data["athlete_count"],
            photo_count=data["photo_count"],
            map=data.get("map"),
            trainer=data["trainer"],
            commute=data["commute"],
            manual=data["manual"],
            private=data["private"],
            visibility=data["visibility"],
            flagged=data["flagged"],
            gear_id=data.get("gear_id"),
            start_latlng=data.get("start_latlng"),
            end_latlng=data.get("end_latlng"),
            average_speed=data["average_speed"],
            max_speed=data["max_speed"],
            average_cadence=data.get("average_cadence"),
            average_watts=data.get("average_watts"),
            weighted_average_watts=data.get("weighted_average_watts"),
            kilojoules=data.get("kilojoules"),
            device_watts=data.get("device_watts", False),
            has_heartrate=data["has_heartrate"],
            average_heartrate=data.get("average_heartrate"),
            max_heartrate=data.get("max_heartrate"),
            heartrate_opt_out=data.get("heartrate_opt_out", False),
            display_hide_heartrate_option=data.get("display_hide_heartrate_option", False),
            elev_high=data.get("elev_high"),
            elev_low=data.get("elev_low"),
            upload_id=data.get("upload_id"),
            upload_id_str=data.get("upload_id_str"),
            external_id=data.get("external_id"),
            from_accepted_tag=data.get("from_accepted_tag", False),
            pr_count=data["pr_count"],
            total_photo_count=data["total_photo_count"],
            has_kudoed=data["has_kudoed"],
        )
        
        detailed_info = str(activity)
        
        # Add additional details if available
        if data.get("description"):
            detailed_info += f"\nDescription: {data['description']}"
        if data.get("calories"):
            detailed_info += f"\nCalories: {data['calories']}"
        if data.get("segment_efforts"):
            detailed_info += f"\nSegment Efforts: {len(data['segment_efforts'])}"
            
        return detailed_info
    
    async def get_athlete_stats(self) -> str:
        """Get athlete's all-time statistics."""
        athlete_data = await self._make_request("GET", "/athlete")
        athlete_id = athlete_data["id"]
        
        data = await self._make_request("GET", f"/athletes/{athlete_id}/stats")
        
        stats = AthleteStats(
            biggest_ride_distance=data["biggest_ride_distance"],
            biggest_climb_elevation_gain=data["biggest_climb_elevation_gain"],
            recent_ride_totals=data["recent_ride_totals"],
            recent_run_totals=data["recent_run_totals"],
            recent_swim_totals=data["recent_swim_totals"],
            ytd_ride_totals=data["ytd_ride_totals"],
            ytd_run_totals=data["ytd_run_totals"],
            ytd_swim_totals=data["ytd_swim_totals"],
            all_ride_totals=data["all_ride_totals"],
            all_run_totals=data["all_run_totals"],
            all_swim_totals=data["all_swim_totals"],
        )
        
        return str(stats)
    
    async def search_activities(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        activity_type: Optional[str] = None
    ) -> str:
        """Search activities by date range and type."""
        params = {"per_page": 200, "page": 1}
        
        # Convert date strings to timestamps if provided
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                params["after"] = int(start_dt.timestamp())
            except ValueError:
                return f"Invalid start_date format. Use YYYY-MM-DD."
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)  # Include end date
                params["before"] = int(end_dt.timestamp())
            except ValueError:
                return f"Invalid end_date format. Use YYYY-MM-DD."
        
        data = await self._make_request("GET", "/athlete/activities", params=params)
        
        activities = []
        for item in data:
            if activity_type and item["type"] != activity_type:
                continue
            
            activity = Activity(
                resource_state=item["resource_state"],
                athlete=item["athlete"],
                name=item["name"],
                distance=item["distance"],
                moving_time=item["moving_time"],
                elapsed_time=item["elapsed_time"],
                total_elevation_gain=item["total_elevation_gain"],
                type=item["type"],
                sport_type=item.get("sport_type", item["type"]),
                workout_type=item.get("workout_type"),
                id=item["id"],
                start_date=item["start_date"],
                start_date_local=item["start_date_local"],
                timezone=item["timezone"],
                utc_offset=item["utc_offset"],
                location_city=item.get("location_city"),
                location_state=item.get("location_state"),
                location_country=item.get("location_country"),
                achievement_count=item["achievement_count"],
                kudos_count=item["kudos_count"],
                comment_count=item["comment_count"],
                athlete_count=item["athlete_count"],
                photo_count=item["photo_count"],
                map=item.get("map"),
                trainer=item["trainer"],
                commute=item["commute"],
                manual=item["manual"],
                private=item["private"],
                visibility=item["visibility"],
                flagged=item["flagged"],
                gear_id=item.get("gear_id"),
                start_latlng=item.get("start_latlng"),
                end_latlng=item.get("end_latlng"),
                average_speed=item["average_speed"],
                max_speed=item["max_speed"],
                average_cadence=item.get("average_cadence"),
                average_watts=item.get("average_watts"),
                weighted_average_watts=item.get("weighted_average_watts"),
                kilojoules=item.get("kilojoules"),
                device_watts=item.get("device_watts", False),
                has_heartrate=item["has_heartrate"],
                average_heartrate=item.get("average_heartrate"),
                max_heartrate=item.get("max_heartrate"),
                heartrate_opt_out=item.get("heartrate_opt_out", False),
                display_hide_heartrate_option=item.get("display_hide_heartrate_option", False),
                elev_high=item.get("elev_high"),
                elev_low=item.get("elev_low"),
                upload_id=item.get("upload_id"),
                upload_id_str=item.get("upload_id_str"),
                external_id=item.get("external_id"),
                from_accepted_tag=item.get("from_accepted_tag", False),
                pr_count=item["pr_count"],
                total_photo_count=item["total_photo_count"],
                has_kudoed=item["has_kudoed"],
            )
            activities.append(activity)
        
        if not activities:
            return f"No activities found for the specified criteria."
        
        result = f"Found {len(activities)} activities"
        if start_date or end_date:
            result += f" between {start_date or 'beginning'} and {end_date or 'now'}"
        if activity_type:
            result += f" of type {activity_type}"
        result += ":\n\n"
        
        for i, activity in enumerate(activities, 1):
            result += f"{i}. {str(activity)}\n\n"
        
        return result