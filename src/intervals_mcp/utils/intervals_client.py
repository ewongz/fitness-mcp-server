"""
Intervals.icu API client utilities.

Provides methods to interact with the intervals.icu API for accessing
activity data, performance metrics, and training analytics.
"""
import base64
import os
import httpx
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from urllib.parse import urlencode

from ..models.intervals_models import (
    Activity, ActivitySummary, ActivityWithIntervals, ActivityStream,
    PowerCurve, ActivityPowerCurve, HRCurve, PaceCurve,
    Athlete, Wellness, Event, BestEfforts,
    ActivitySearchResult, PerformanceAnalysis
)


class IntervalsClient:
    """Client for interacting with the intervals.icu API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://intervals.icu"):
        """Initialize the client with API credentials."""
        self.api_key = api_key or os.getenv("INTERVALS_API_KEY")
        self.athlete_id = os.getenv("INTERVALS_ATHLETE_ID")
        self.base_url = base_url.rstrip("/")
        
        if not self.api_key:
            raise ValueError("API key is required. Set INTERVALS_API_KEY environment variable or pass api_key parameter.")
        
        b64encoded_creds = base64.b64encode(f"API_KEY:{self.api_key}".encode("utf-8")).decode("utf-8")
        headers={
            "Authorization": f"Basic {b64encoded_creds}",
            "accept": "*/*"
        }
        self._client = httpx.AsyncClient(
            headers=headers,
            timeout=30.0
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to intervals.icu API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            
            # Handle empty responses
            if response.status_code == 204 or not response.content:
                return {}
                
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid API key or unauthorized access")
            elif e.response.status_code == 403:
                raise ValueError("Access forbidden - check permissions")
            elif e.response.status_code == 404:
                raise ValueError("Resource not found")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise ValueError(f"API request failed: {e.response.status_code} {e.response.text}")
        except httpx.RequestError as e:
            raise ValueError(f"Request error: {str(e)}")
    
    # Athlete methods
    async def get_athlete(self, athlete_id: str) -> Athlete:
        """Get athlete profile."""
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}")
        return Athlete(**data)
    
    # Activity methods
    async def get_activities(
        self,
        athlete_id: str,
        limit: int = 50,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        activity_type: Optional[str] = None
    ) -> List[ActivitySummary]:
        """Get list of activities for an athlete."""
        params = {"limit": limit}
        
        if start_date:
            params["oldest"] = start_date if isinstance(start_date, str) else start_date.isoformat()
        if end_date:
            params["newest"] = end_date if isinstance(end_date, str) else end_date.isoformat()
        if activity_type:
            params["type"] = activity_type
            
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/activities", params=params)
        return [ActivitySummary(**activity) for activity in data]
    
    async def get_activity(self, activity_id: str, include_intervals: bool = False) -> Union[Activity, ActivityWithIntervals]:
        """Get detailed activity data."""
        params = {"intervals": "true"} if include_intervals else None
        data = await self._make_request("GET", f"/api/v1/activity/{activity_id}", params=params)
        
        if include_intervals and "icu_intervals" in data:
            return ActivityWithIntervals(**data)
        else:
            return Activity(**data)
    
    async def get_activity_streams(self, activity_id: str) -> List[ActivityStream]:
        """Get activity stream data (power, heart rate, GPS, etc.)."""
        data = await self._make_request("GET", f"/api/v1/activity/{activity_id}/streams")
        return [ActivityStream(**stream) for stream in data]
    
    async def search_activities(
        self,
        athlete_id: str,
        query: Optional[str] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        activity_type: Optional[str] = None,
        limit: int = 50
    ) -> ActivitySearchResult:
        """Search activities with filters."""
        params = {"limit": limit}
        
        if query:
            params["q"] = query
        if start_date:
            params["oldest"] = start_date if isinstance(start_date, str) else start_date.isoformat()
        if end_date:
            params["newest"] = end_date if isinstance(end_date, str) else end_date.isoformat()
        if activity_type:
            params["type"] = activity_type
            
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/activities/search", params=params)
        activities = [ActivitySummary(**activity) for activity in data.get("activities", data)]
        
        return ActivitySearchResult(
            activities=activities,
            total_count=data.get("total_count"),
            page=data.get("page"),
            per_page=data.get("per_page")
        )
    
    async def get_activities_around_date(
        self,
        athlete_id: str,
        target_date: Union[str, date],
        days_before: int = 7,
        days_after: int = 7
    ) -> List[ActivitySummary]:
        """Get activities around a specific date."""
        params = {
            "date": target_date if isinstance(target_date, str) else target_date.isoformat(),
            "before": days_before,
            "after": days_after
        }
        
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/activities-around", params=params)
        return [ActivitySummary(**activity) for activity in data]
    
    # Performance analysis methods
    async def get_power_curve(self, athlete_id: str, sport: Optional[str] = None) -> PowerCurve:
        """Get athlete's power curve."""
        params = {"sport": sport} if sport else None
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/power-curves", params=params)
        return PowerCurve(**data)
    
    async def get_activity_power_curve(self, activity_id: str) -> ActivityPowerCurve:
        """Get power curve for specific activity."""
        data = await self._make_request("GET", f"/api/v1/activity/{activity_id}/power-curve")
        return ActivityPowerCurve(**data)
    
    async def get_hr_curve(self, athlete_id: str, sport: Optional[str] = None) -> HRCurve:
        """Get athlete's heart rate curve."""
        params = {"sport": sport} if sport else None
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/hr-curves", params=params)
        return HRCurve(**data)
    
    async def get_pace_curve(self, athlete_id: str, sport: Optional[str] = None) -> PaceCurve:
        """Get athlete's pace curve."""
        params = {"sport": sport} if sport else None
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/pace-curves", params=params)
        return PaceCurve(**data)
    
    async def get_activity_best_efforts(self, activity_id: str) -> BestEfforts:
        """Get best efforts for an activity."""
        data = await self._make_request("GET", f"/api/v1/activity/{activity_id}/best-efforts")
        return BestEfforts(**data)
    
    async def get_performance_analysis(
        self,
        athlete_id: str,
        sport: Optional[str] = None,
        activity_id: Optional[str] = None
    ) -> PerformanceAnalysis:
        """Get comprehensive performance analysis."""
        analysis = PerformanceAnalysis()
        
        try:
            # Get power curve
            analysis.power_curve = await self.get_power_curve(athlete_id, sport)
        except Exception:
            pass  # Not all athletes have power data
            
        try:
            # Get HR curve  
            analysis.hr_curve = await self.get_hr_curve(athlete_id, sport)
        except Exception:
            pass
            
        try:
            # Get pace curve
            analysis.pace_curve = await self.get_pace_curve(athlete_id, sport)
        except Exception:
            pass
            
        if activity_id:
            try:
                # Get activity-specific best efforts
                analysis.best_efforts = await self.get_activity_best_efforts(activity_id)
            except Exception:
                pass
                
        return analysis
    
    # Wellness methods
    async def get_wellness(self, athlete_id: str, date_str: Union[str, date]) -> Wellness:
        """Get wellness data for a specific date."""
        date_param = date_str if isinstance(date_str, str) else date_str.isoformat()
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/wellness/{date_param}")
        return Wellness(**data)
    
    async def get_wellness_range(
        self,
        athlete_id: str,
        start_date: Union[str, date],
        end_date: Union[str, date]
    ) -> List[Wellness]:
        """Get wellness data for a date range."""
        params = {
            "oldest": start_date if isinstance(start_date, str) else start_date.isoformat(),
            "newest": end_date if isinstance(end_date, str) else end_date.isoformat()
        }
        
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/wellness", params=params)
        return [Wellness(**record) for record in data]
    
    # Calendar/Events methods
    async def get_events(
        self,
        athlete_id: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        category: Optional[str] = None
    ) -> List[Event]:
        """Get calendar events for date range."""
        params = {
            "oldest": start_date if isinstance(start_date, str) else start_date.isoformat(),
            "newest": end_date if isinstance(end_date, str) else end_date.isoformat()
        }
        
        if category:
            params["category"] = category
            
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/events", params=params)
        return [Event(**event) for event in data]
    
    async def get_event(self, athlete_id: str, event_id: int) -> Event:
        """Get specific event."""
        data = await self._make_request("GET", f"/api/v1/athlete/{athlete_id}/events/{event_id}")
        return Event(**data)
    
    # Export methods  
    async def export_activities_csv(
        self,
        athlete_id: str,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None
    ) -> str:
        """Export activities as CSV."""
        params = {}
        if start_date:
            params["oldest"] = start_date if isinstance(start_date, str) else start_date.isoformat()
        if end_date:
            params["newest"] = end_date if isinstance(end_date, str) else end_date.isoformat()
            
        response = await self._client.get(
            f"{self.base_url}/api/v1/athlete/{athlete_id}/activities.csv",
            params=params
        )
        response.raise_for_status()
        return response.text
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()