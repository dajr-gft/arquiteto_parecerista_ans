#!/usr/bin/env python
"""Test script to verify root_agent import"""
import sys

try:
    from routes import root_agent
    print(f"✓ Success! root_agent imported")
    print(f"  Name: {root_agent.name}")
    print(f"  Model: {root_agent.model}")
    print(f"  Description: {root_agent.description}")
except Exception as e:
    print(f"✗ Error importing root_agent:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

