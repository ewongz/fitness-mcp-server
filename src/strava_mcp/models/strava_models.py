from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Athlete:
    """Strava athlete model."""
    id: int
    username: Optional[str]
    resource_state: int
    firstname: str
    lastname: str
    bio: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    sex: Optional[str]
    premium: bool
    summit: bool
    created_at: str
    updated_at: str
    badge_type_id: Optional[int]
    weight: Optional[float]
    profile_medium: Optional[str]
    profile: Optional[str]
    friend: Optional[str]
    follower: Optional[str]
    
    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname} (@{self.username}) - {self.city}, {self.state}"

@dataclass
class Activity:
    """Strava activity model."""
    resource_state: int
    athlete: Dict[str, Any]
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    type: str
    sport_type: str
    workout_type: Optional[int]
    id: int
    start_date: str
    start_date_local: str
    timezone: str
    utc_offset: int
    location_city: Optional[str]
    location_state: Optional[str]
    location_country: Optional[str]
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    map: Optional[Dict[str, Any]]
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    visibility: str
    flagged: bool
    gear_id: Optional[str]
    start_latlng: Optional[List[float]]
    end_latlng: Optional[List[float]]
    average_speed: float
    max_speed: float
    average_cadence: Optional[float]
    average_watts: Optional[float]
    weighted_average_watts: Optional[int]
    kilojoules: Optional[float]
    device_watts: bool
    has_heartrate: bool
    average_heartrate: Optional[float]
    max_heartrate: Optional[float]
    heartrate_opt_out: bool
    display_hide_heartrate_option: bool
    elev_high: Optional[float]
    elev_low: Optional[float]
    upload_id: Optional[int]
    upload_id_str: Optional[str]
    external_id: Optional[str]
    from_accepted_tag: bool
    pr_count: int
    total_photo_count: int
    has_kudoed: bool
    
    def __str__(self) -> str:
        distance_km = self.distance / 1000
        moving_minutes = self.moving_time // 60
        moving_seconds = self.moving_time % 60
        pace_per_km = (self.moving_time / 60) / distance_km if distance_km > 0 else 0
        
        return (f"{self.name} - {self.type}\n"
                f"Distance: {distance_km:.2f}km\n"
                f"Time: {moving_minutes}:{moving_seconds:02d}\n"
                f"Pace: {pace_per_km:.2f} min/km\n"
                f"Elevation: {self.total_elevation_gain}m\n"
                f"Date: {self.start_date_local}")

@dataclass
class AthleteStats:
    """Strava athlete statistics model."""
    biggest_ride_distance: float
    biggest_climb_elevation_gain: float
    recent_ride_totals: Dict[str, Any]
    recent_run_totals: Dict[str, Any]
    recent_swim_totals: Dict[str, Any]
    ytd_ride_totals: Dict[str, Any]
    ytd_run_totals: Dict[str, Any]
    ytd_swim_totals: Dict[str, Any]
    all_ride_totals: Dict[str, Any]
    all_run_totals: Dict[str, Any]
    all_swim_totals: Dict[str, Any]
    
    def __str__(self) -> str:
        return (f"All-Time Stats:\n"
                f"Rides: {self.all_ride_totals.get('count', 0)} activities, "
                f"{self.all_ride_totals.get('distance', 0)/1000:.1f}km\n"
                f"Runs: {self.all_run_totals.get('count', 0)} activities, "
                f"{self.all_run_totals.get('distance', 0)/1000:.1f}km\n"
                f"Swims: {self.all_swim_totals.get('count', 0)} activities, "
                f"{self.all_swim_totals.get('distance', 0)/1000:.1f}km\n"
                f"Biggest Ride: {self.biggest_ride_distance/1000:.1f}km\n"
                f"Biggest Climb: {self.biggest_climb_elevation_gain}m")

@dataclass
class ActivityStream:
    """Strava activity stream data."""
    type: str
    data: List[Any]
    series_type: str
    original_size: int
    resolution: str
    
    def __str__(self) -> str:
        return f"{self.type} stream: {len(self.data)} points"

@dataclass 
class Segment:
    """Strava segment model."""
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: List[float]
    end_latlng: List[float]
    elevation_profile: Optional[str]
    climb_category: int
    city: str
    state: str
    country: str
    private: bool
    hazardous: bool
    starred: bool
    
    def __str__(self) -> str:
        return (f"{self.name}\n"
                f"Distance: {self.distance/1000:.2f}km\n"
                f"Grade: {self.average_grade:.1f}% avg, {self.maximum_grade:.1f}% max\n"
                f"Elevation: {self.elevation_low}m - {self.elevation_high}m\n"
                f"Location: {self.city}, {self.state}")

@dataclass
class Club:
    """Strava club model."""
    id: int
    resource_state: int
    name: str
    profile_medium: str
    profile: str
    cover_photo: Optional[str]
    cover_photo_small: Optional[str]
    sport_type: str
    activity_types: List[str]
    city: str
    state: str
    country: str
    private: bool
    member_count: int
    featured: bool
    verified: bool
    url: str
    
    def __str__(self) -> str:
        return f"{self.name} - {self.member_count} members ({self.city}, {self.state})"