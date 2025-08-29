#!/usr/bin/env python3
"""
Run the intervals.icu MCP server.
"""

import asyncio
from src.intervals_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())