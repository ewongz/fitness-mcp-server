"""
Intervals.icu API data models.

Based on the intervals.icu OpenAPI specification.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


class ActivityStream(BaseModel):
    """Time-series data stream for an activity (power, heart rate, etc.)."""
    type: str
    name: Optional[str] = None
    data: List[Union[int, float]] = []
    data2: Optional[List[Union[int, float]]] = None
    anomalies: Optional[List[int]] = None


class Interval(BaseModel):
    """Activity interval/segment with detailed metrics."""
    id: Optional[int] = None
    start_index: int
    end_index: int
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    
    # Power metrics
    average_watts: Optional[float] = None
    max_watts: Optional[float] = None
    min_watts: Optional[float] = None
    normalized_watts: Optional[float] = None
    variability_index: Optional[float] = None
    intensity: Optional[float] = None
    
    # Heart rate metrics
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    min_heartrate: Optional[float] = None
    
    # Speed/pace metrics
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    distance: Optional[float] = None
    moving_time: Optional[int] = None
    elapsed_time: Optional[int] = None
    
    # Cadence
    average_cadence: Optional[float] = None
    max_cadence: Optional[float] = None
    
    # Environment
    total_elevation_gain: Optional[float] = None
    average_grade: Optional[float] = None
    
    # Training metrics
    training_load: Optional[float] = None
    zone_time: Optional[List[int]] = None
    
    # Analysis
    name: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None


class IntervalGroup(BaseModel):
    """Group of intervals with aggregate statistics."""
    name: str
    color: Optional[str] = None
    intervals: List[int] = []
    
    # Aggregate metrics (computed from intervals)
    total_time: Optional[int] = None
    total_distance: Optional[float] = None
    average_power: Optional[float] = None
    average_heartrate: Optional[float] = None
    total_training_load: Optional[float] = None


class PowerCurveEntry(BaseModel):
    """Single entry in a power curve."""
    secs: int
    watts: float
    watts_per_kg: Optional[float] = None
    date: Optional[datetime] = None
    activity_id: Optional[str] = None


class PowerCurve(BaseModel):
    """Power curve analysis data."""
    secs: List[int]
    values: List[float]
    watts_per_kg: Optional[List[float]] = None
    dates: Optional[List[datetime]] = None
    activity_ids: Optional[List[str]] = None
    percentiles: Optional[Dict[str, List[float]]] = None


class ActivityPowerCurve(BaseModel):
    """Activity-specific power curve."""
    id: str
    start_date_local: datetime
    watts: List[float]
    weight: Optional[float] = None


class HRCurve(BaseModel):
    """Heart rate curve analysis."""
    secs: List[int]
    values: List[float]
    dates: Optional[List[datetime]] = None
    activity_ids: Optional[List[str]] = None


class PaceCurve(BaseModel):
    """Pace curve analysis."""
    secs: List[int]
    values: List[float]  # pace in seconds per meter
    dates: Optional[List[datetime]] = None
    activity_ids: Optional[List[str]] = None


class Effort(BaseModel):
    """Best effort segment."""
    start_index: int
    end_index: int
    distance: float
    watts: Optional[float] = None
    pace: Optional[float] = None
    heartrate: Optional[float] = None
    moving_time: int
    rank: Optional[int] = None


class BestEfforts(BaseModel):
    """Collection of best effort segments."""
    power: Optional[List[Effort]] = None
    pace: Optional[List[Effort]] = None
    hr: Optional[List[Effort]] = None


class ActivitySummary(BaseModel):
    """Summary view of an activity."""
    id: str
    name: str
    type: str
    start_date_local: datetime
    
    # Duration and distance
    moving_time: Optional[int] = None
    elapsed_time: Optional[int] = None
    distance: Optional[float] = None
    
    # Power metrics
    average_watts: Optional[float] = None
    max_watts: Optional[float] = None
    icu_ftp: Optional[float] = None
    icu_weighted_avg_watts: Optional[float] = None
    icu_training_load: Optional[float] = None
    
    # Heart rate
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    
    # Speed/pace
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    
    # Environment
    total_elevation_gain: Optional[float] = None
    
    # Training status
    icu_atl: Optional[float] = None  # Acute training load (fatigue)
    icu_ctl: Optional[float] = None  # Chronic training load (fitness)
    icu_ramp_rate: Optional[float] = None
    icu_form: Optional[float] = None  # Form (fitness - fatigue)


class Activity(BaseModel):
    """Complete activity/workout data."""
    id: str
    name: str
    description: Optional[str] = None
    type: str
    start_date_local: datetime
    timezone: Optional[str] = None
    
    # Duration and distance
    moving_time: Optional[int] = None
    elapsed_time: Optional[int] = None
    distance: Optional[float] = None
    
    # Power metrics
    average_watts: Optional[float] = None
    max_watts: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    icu_ftp: Optional[float] = None
    icu_weighted_avg_watts: Optional[float] = None
    icu_training_load: Optional[float] = None
    normalized_watts: Optional[float] = None
    intensity_factor: Optional[float] = None
    variability_index: Optional[float] = None
    
    # Heart rate
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    
    # Speed/pace
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    pace: Optional[float] = None
    
    # Cadence
    average_cadence: Optional[float] = None
    max_cadence: Optional[float] = None
    
    # Environment
    total_elevation_gain: Optional[float] = None
    start_latlng: Optional[List[float]] = None
    end_latlng: Optional[List[float]] = None
    weather_temp: Optional[float] = None
    weather_humidity: Optional[float] = None
    weather_wind_speed: Optional[float] = None
    
    # Training metrics
    icu_atl: Optional[float] = None  # Acute training load
    icu_ctl: Optional[float] = None  # Chronic training load
    icu_ramp_rate: Optional[float] = None
    icu_form: Optional[float] = None
    icu_recovery_time: Optional[int] = None
    
    # Equipment
    power_meter: Optional[str] = None
    power_meter_serial: Optional[str] = None
    power_meter_battery: Optional[float] = None
    
    # Zone times (seconds in each zone)
    power_zone_times: Optional[List[int]] = None
    hr_zone_times: Optional[List[int]] = None
    pace_zone_times: Optional[List[int]] = None
    
    # External platform data
    strava_id: Optional[str] = None
    garmin_id: Optional[str] = None
    
    # Files and attachments
    has_power: Optional[bool] = None
    has_heartrate: Optional[bool] = None
    has_cadence: Optional[bool] = None
    has_gps: Optional[bool] = None
    
    # Analysis
    achievements: Optional[List[str]] = None
    
    # Created/updated
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class ActivityWithIntervals(Activity):
    """Activity with detailed interval data."""
    icu_intervals: Optional[List[Interval]] = None
    icu_groups: Optional[List[IntervalGroup]] = None


class ZoneTime(BaseModel):
    """Time spent in training zones."""
    z1: int = 0
    z2: int = 0
    z3: int = 0
    z4: int = 0
    z5: int = 0
    z6: int = 0
    z7: int = 0


class SportSettings(BaseModel):
    """Sport-specific settings and zones."""
    sport: str
    ftp: Optional[float] = None
    ftp_date: Optional[datetime] = None
    
    # Power zones
    power_zone_names: Optional[List[str]] = None
    power_zone_bounds: Optional[List[float]] = None
    
    # Heart rate zones
    hr_zone_names: Optional[List[str]] = None
    hr_zone_bounds: Optional[List[float]] = None
    
    # Pace zones
    pace_zone_names: Optional[List[str]] = None
    pace_zone_bounds: Optional[List[float]] = None


class Athlete(BaseModel):
    """Athlete profile and settings."""
    id: str
    name: str
    email: Optional[str] = None
    username: Optional[str] = None
    
    # Personal info
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    weight: Optional[float] = None
    
    # Preferences
    measurement_preference: Optional[str] = None  # metric/imperial
    training_view: Optional[str] = None
    
    # Training settings
    sports_settings: Optional[List[SportSettings]] = None
    
    # Platform connections
    strava_athlete_id: Optional[str] = None
    garmin_user_id: Optional[str] = None
    polar_user_id: Optional[str] = None
    
    # Sync settings
    auto_sync: Optional[bool] = None
    sync_strava: Optional[bool] = None
    sync_garmin: Optional[bool] = None
    sync_polar: Optional[bool] = None
    
    # Privacy settings
    privacy: Optional[str] = None
    show_email: Optional[bool] = None
    
    # Created/updated
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class Wellness(BaseModel):
    """Daily wellness metrics."""
    id: str  # Date in ISO format
    athlete_id: str
    
    # Sleep
    sleep_quality: Optional[int] = None  # 1-5 scale
    sleep_hours: Optional[float] = None
    
    # Health metrics
    resting_hr: Optional[int] = None
    hrv: Optional[float] = None
    weight: Optional[float] = None
    body_fat: Optional[float] = None
    
    # Subjective measures (typically 1-5 scale)
    stress: Optional[int] = None
    fatigue: Optional[int] = None
    soreness: Optional[int] = None
    mood: Optional[int] = None
    motivation: Optional[int] = None
    
    # Menstrual cycle tracking
    menstrual_flow: Optional[int] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Created/updated
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class Event(BaseModel):
    """Calendar event (workout, race, note)."""
    id: Optional[int] = None
    athlete_id: str
    start_date_local: datetime
    
    # Event info
    name: Optional[str] = None
    description: Optional[str] = None
    category: str  # WORKOUT, RACE, NOTE, etc.
    type: Optional[str] = None
    
    # Duration
    moving_time: Optional[int] = None
    
    # Planning targets
    target_power: Optional[float] = None
    target_heartrate: Optional[float] = None
    target_pace: Optional[float] = None
    target_distance: Optional[float] = None
    target_training_load: Optional[float] = None
    
    # Workout file
    workout_doc: Optional[str] = None  # Intervals.icu workout format
    
    # Completion status
    completed: Optional[bool] = None
    activity_id: Optional[str] = None
    
    # Privacy
    hide_from_athlete: Optional[bool] = None
    athlete_cannot_edit: Optional[bool] = None
    
    # External references
    external_id: Optional[str] = None
    
    # Created/updated
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class ActivitySearchResult(BaseModel):
    """Search result containing activities."""
    activities: List[ActivitySummary]
    total_count: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class PerformanceAnalysis(BaseModel):
    """Performance analysis data combining multiple metrics."""
    power_curve: Optional[PowerCurve] = None
    hr_curve: Optional[HRCurve] = None
    pace_curve: Optional[PaceCurve] = None
    best_efforts: Optional[BestEfforts] = None
    zone_distribution: Optional[Dict[str, ZoneTime]] = None