"""Intervals.icu MCP Server package."""

from .server import app
from .utils import IntervalsClient
from .models import (
    Activity,
    ActivitySummary,
    ActivityWithIntervals,
    Athlete,
    PerformanceAnalysis,
    Wellness,
    Event,
)

__all__ = [
    "app",
    "IntervalsClient", 
    "Activity",
    "ActivitySummary",
    "ActivityWithIntervals",
    "Athlete",
    "PerformanceAnalysis",
    "Wellness",
    "Event",
]