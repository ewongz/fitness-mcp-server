# Fitness Data MCP Servers

Model Context Protocol (MCP) servers that enable Claude to access your fitness and training data. This project includes servers for both Strava and intervals.icu, providing comprehensive tools and resources for analyzing your athletic performance, activities, and training metrics.

## 🏃‍♂️ **Strava MCP Server**
Access your Strava activities, athlete profile, and basic performance statistics.

## 📊 **Intervals.icu MCP Server** ⭐ *Featured*
Advanced training analytics with power curves, detailed workout analysis, wellness tracking, and comprehensive performance metrics.

## Features

---

## 🏃‍♂️ **Strava MCP Server Features**

### Available Tools
- **`get_activities`** - Fetch recent activities with filtering options
- **`get_activity_details`** - Get detailed information about specific activities
- **`get_athlete_stats`** - Retrieve all-time athlete statistics
- **`search_activities`** - Search activities by date range and activity type

### Available Resources
- **`strava://activities`** - Recent activities feed
- **`strava://athlete`** - Athlete profile information
- **`strava://stats`** - All-time statistics summary

---

## 📊 **Intervals.icu MCP Server Features** ⭐

### 🛠️ Advanced Training Tools (11 Tools)
- **`get_activities`** - List activities with advanced filtering (date, type, limit)
- **`get_activity_details`** - Detailed activity data with optional interval analysis
- **`get_activity_streams`** - Time-series data (power, heart rate, GPS, cadence, speed)
- **`search_activities`** - Full-text search across activities and advanced filters
- **`get_power_curve`** - Athlete's power curve analysis (peak power at all durations)
- **`get_activity_power_curve`** - Activity-specific power analysis
- **`get_performance_analysis`** - Comprehensive performance metrics (power, HR, pace curves)
- **`get_best_efforts`** - Best effort segments and achievements for activities
- **`get_wellness_data`** - Sleep, HRV, stress, and wellness metrics
- **`get_training_calendar`** - Planned workouts, races, and training events
- **`export_activities_csv`** - Export training data for external analysis

### 📈 Rich Data Resources (5 Resources)
- **`intervals://activities`** - Recent activities with detailed metrics
- **`intervals://athlete`** - Complete athlete profile and training settings
- **`intervals://performance`** - Power curves, heart rate analysis, and performance metrics
- **`intervals://wellness`** - Sleep, HRV, and wellness tracking data
- **`intervals://calendar`** - Training calendar with planned workouts and races

### 🎯 Advanced Analytics Capabilities
- **Power Analysis**: Mean maximal power curves, FTP tracking, power-to-weight ratios
- **Heart Rate Analysis**: HR curves, zone distribution, decoupling analysis
- **Pace Analysis**: Pace curves for running, grade-adjusted pace, best efforts
- **Interval Analysis**: Structured workout analysis, interval statistics, training zones
- **Wellness Tracking**: Sleep quality, HRV, stress, fatigue, and recovery metrics
- **Training Load**: CTL/ATL/TSB (fitness/fatigue/form), training stress tracking
- **Multi-Sport Support**: Cycling, running, swimming with sport-specific zones and metrics

### 🎯 Supported Activity Types
**Cycling**: Road, Mountain, Track, Gravel, E-bike, Indoor/Trainer
**Running**: Road, Trail, Track, Treadmill
**Swimming**: Pool, Open Water
**Other**: Triathlon, Walking, Hiking, Cross-training, and 30+ sport types

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Claude Desktop app
- **For Strava**: Strava Developer Account and API access token
- **For intervals.icu**: intervals.icu account and API key

---

## 🏃‍♂️ **Strava MCP Server Setup**

### 1. Get Strava API Access

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application:
   - **Application Name**: `fitness-mcp-server`
   - **Category**: `Data Importer`
   - **Authorization Callback Domain**: `localhost`
   - Upload any icon image
3. Copy your **Access Token** (you'll need this for the next step)

### 2. Configure and Test Strava

```bash
# Clone the repository
git clone <repository-url>
cd fitness-mcp-server

# Install dependencies
uv sync

# Copy the example environment file
cp .env.example .env

# Edit .env and add your Strava access token
# STRAVA_ACCESS_TOKEN=your_actual_access_token_here

# Test the Strava server
uv run python run_server.py
```

---

## 📊 **Intervals.icu MCP Server Setup** ⭐

### 1. Get intervals.icu API Access

1. Go to [intervals.icu Developer Settings](https://intervals.icu/settings/developer)
2. Click **"Create API Key"**
3. Copy your API key
4. Your **Athlete ID** is in your profile URL: `https://intervals.icu/athletes/[YOUR_ID]`

### 2. Configure and Test intervals.icu

```bash
# Edit .env and add your intervals.icu credentials
# INTERVALS_API_KEY=your_intervals_icu_api_key_here
# INTERVALS_ATHLETE_ID=your_athlete_id_here

# Test the intervals.icu connection
python test_intervals.py

# Run the intervals.icu server
python run_intervals_server.py
```

---

## ⚙️ **Claude Desktop Configuration**

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

### Option 1: intervals.icu Server Only (Recommended)
```json
{
  "mcpServers": {
    "intervals": {
      "command": "uv",
      "args": ["--directory", "/path/to/fitness-mcp-server", "run", "python", "run_intervals_server.py"],
      "cwd": "/path/to/fitness-mcp-server"
    }
  }
}
```

### Option 2: Both Servers
```json
{
  "mcpServers": {
    "strava": {
      "command": "uv",
      "args": ["--directory", "/path/to/fitness-mcp-server", "run", "python", "run_server.py"],
      "cwd": "/path/to/fitness-mcp-server"
    },
    "intervals": {
      "command": "uv",
      "args": ["--directory", "/path/to/fitness-mcp-server", "run", "python", "run_intervals_server.py"],
      "cwd": "/path/to/fitness-mcp-server"
    }
  }
}
```

Replace `/path/to/fitness-mcp-server` with the actual path to your project directory.

### Restart Claude Desktop

Quit and restart Claude Desktop for the MCP server configuration to take effect.

## Usage

Once configured, you can ask Claude natural language questions about your fitness data. The intervals.icu server provides much more comprehensive analytics than Strava.

---

### 🏃‍♂️ **Strava Server Examples**
- **"Show me my recent Strava activities"**
- **"What are my all-time running statistics?"**
- **"Get my cycling activities from last week"**
- **"Show me my longest run this month"**

---

### 📊 **Intervals.icu Server Examples** ⭐

#### **Basic Activity Queries**
- **"Show me my recent training activities"**
- **"Get my cycling workouts from this month"**  
- **"Find my hardest workout this week"**
- **"Export my activities from January as CSV"**

#### **Advanced Performance Analysis**
- **"Show me my power curve for cycling"**
- **"Analyze my heart rate trends over the last month"**
- **"What are my best 20-minute power efforts this year?"**
- **"Compare my recent FTP progress"**
- **"Show my training load and form trends"**

#### **Detailed Workout Analysis**
- **"Analyze the intervals in my workout from yesterday"**
- **"Get the power data streams for activity ID 12345"**
- **"Show me the time-series data for my last race"**
- **"What were my best efforts in my last cycling workout?"**

#### **Wellness and Recovery**
- **"How has my sleep quality been this week?"**
- **"Show my HRV trends for the last month"**
- **"What's my stress level pattern?"**
- **"How is my recovery looking based on wellness data?"**

#### **Training Planning**
- **"What workouts do I have planned this week?"**
- **"Show my upcoming races and events"**
- **"What's on my training calendar for next month?"**

#### **Advanced Analytics**
- **"Analyze my power-to-weight ratio improvements"**
- **"Show my cycling efficiency metrics"**
- **"Compare my running pace across different terrains"**
- **"What are my zone distribution patterns?"**

Claude will automatically use the appropriate MCP tools to fetch and present your comprehensive training data with detailed analytics.

## Architecture

### Project Structure
```
fitness-mcp-servers/
├── src/
│   ├── strava_mcp/                    # Strava MCP Server
│   │   ├── server.py                  # Strava MCP server implementation
│   │   ├── models/strava_models.py    # Strava data models
│   │   └── utils/strava_client.py     # Strava API client
│   └── intervals_mcp/                 # intervals.icu MCP Server ⭐
│       ├── server.py                  # intervals.icu MCP server implementation
│       ├── models/intervals_models.py # intervals.icu data models (comprehensive)
│       └── utils/intervals_client.py  # intervals.icu API client (full-featured)
├── run_server.py                      # Strava server entry point
├── run_intervals_server.py            # intervals.icu server entry point
├── test_intervals.py                  # intervals.icu connection test
├── .env.example                       # Environment template (both services)
└── pyproject.toml                     # Project configuration
```

### Key Differences Between Servers

| Feature | Strava MCP | intervals.icu MCP ⭐ |
|---------|------------|-------------------|
| **Activities** | Basic list, search | Advanced filtering, full-text search |
| **Activity Details** | Summary data | Detailed metrics + intervals + streams |
| **Performance Data** | Basic stats | Power curves, HR analysis, pace curves |
| **Training Analytics** | ❌ | ✅ Training load, CTL/ATL/TSB, zones |
| **Wellness Tracking** | ❌ | ✅ Sleep, HRV, stress, recovery |
| **Workout Analysis** | ❌ | ✅ Intervals, segments, structured analysis |
| **Time-Series Data** | ❌ | ✅ Power, HR, GPS, cadence streams |
| **Training Calendar** | ❌ | ✅ Planned workouts, races, events |
| **Data Export** | ❌ | ✅ CSV export with full metrics |

## Token Management

### Strava
⚠️ **Important**: Strava access tokens expire every 6 hours. For continuous usage, you may need to:
1. Manually refresh tokens periodically, or
2. Implement OAuth flow with refresh tokens (advanced)

For personal use, manually updating the token in your `.env` file when it expires is sufficient.

### intervals.icu
✅ **Simple**: intervals.icu API keys are long-lived and don't expire frequently. Much easier to manage for personal use.

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'dotenv'"**
- Run `uv sync` to install dependencies
- Ensure you're using `uv run python` or just `python` with proper environment

**"Invalid API key" (intervals.icu)**
- Verify your `INTERVALS_API_KEY` in the `.env` file
- Check your API key at https://intervals.icu/settings/developer
- Ensure your `INTERVALS_ATHLETE_ID` matches your profile

**"Invalid or expired Strava access token"**
- Get a new access token from your Strava API application
- Update the `STRAVA_ACCESS_TOKEN` in your `.env` file

**"MCP server not connecting in Claude"**
- Check the file path in `claude_desktop_config.json` is correct
- Restart Claude Desktop after configuration changes
- Test the server runs without errors: `python test_intervals.py`

### Debug Mode

```bash
# Test intervals.icu connection
python test_intervals.py

# Run intervals.icu server directly (recommended)
python run_intervals_server.py

# Run Strava server
uv run python run_server.py
```

## Development

### Adding New Tools

- **Strava**: Extend `@app.list_tools()` and `@app.call_tool()` in `src/strava_mcp/server.py`
- **intervals.icu**: Extend handlers in `src/intervals_mcp/server.py` (more comprehensive API available)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test with your fitness data (Strava and/or intervals.icu)
5. Submit a pull request

## Why intervals.icu? ⭐

intervals.icu offers significantly more comprehensive training data access compared to Strava:

- **Complete Training Analytics**: Power curves, training load modeling, fitness/fatigue tracking
- **Detailed Workout Analysis**: Interval breakdowns, structured training analysis, best efforts  
- **Wellness Integration**: Sleep, HRV, stress tracking for comprehensive health monitoring
- **Advanced Performance Metrics**: Sport-specific zones, equipment tracking, weather correlation
- **Time-Series Data Access**: Full access to power, heart rate, GPS, and sensor data streams
- **Training Planning**: Calendar integration with planned workouts and periodization
- **Better API**: More stable, comprehensive, and easier to use than Strava's API

For serious athletes and coaches, the intervals.icu MCP server provides AI assistants with the depth of data needed for meaningful training insights and performance analysis.

## License

MIT License - see LICENSE file for details.

## Disclaimer

This project is not affiliated with Strava or intervals.icu. It uses the official APIs to access your personal fitness data. Your data remains private and is only accessible through your own MCP server instance. Always review API permissions and terms of service for each platform.