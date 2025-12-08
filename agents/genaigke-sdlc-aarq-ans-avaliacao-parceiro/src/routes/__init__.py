"""
Routes module for ADK Web Server
Exposes root_agent for the ANS Expert Agent
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import root_agent - handle both relative and absolute imports
try:
    from .agent import root_agent
except ImportError:
    from routes.agent import root_agent

__all__ = ['root_agent']

