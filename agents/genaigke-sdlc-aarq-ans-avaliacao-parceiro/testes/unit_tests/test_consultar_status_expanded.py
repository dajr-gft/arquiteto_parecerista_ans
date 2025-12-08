"""Testes expandidos para routes/tools/consultar_status.py."""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_get_status_returns_json():
    """Test get_status returns valid JSON."""
    from routes.tools.consultar_status import get_status

    result = get_status()

    assert result is not None
    # Parse JSON to ensure it's valid
    data = json.loads(result)
    assert "status" in data
    assert data["status"] == "online"


def test_get_status_includes_service_info():
    """Test get_status includes service information."""
    from routes.tools.consultar_status import get_status

    result = get_status()
    data = json.loads(result)

    assert "service" in data
    assert "version" in data


def test_get_health_returns_json():
    """Test get_health returns valid JSON."""
    from routes.tools.consultar_status import get_health

    result = get_health()

    assert result is not None
    data = json.loads(result)
    assert "status" in data
    assert data["status"] == "healthy"


def test_get_health_includes_timestamp():
    """Test that get_health includes timestamp."""
    from routes.tools.consultar_status import get_health

    result = get_health()
    data = json.loads(result)

    assert "timestamp" in data
    # Timestamp should be ISO format string
    assert isinstance(data["timestamp"], str)


def test_get_status_with_environment_vars():
    """Test get_status with environment variables set."""
    from routes.tools.consultar_status import get_status

    with patch.dict('os.environ', {'GOOGLE_CLOUD_PROJECT': 'test-project'}):
        result = get_status()
        data = json.loads(result)

        assert data["project_id"] == "test-project"

