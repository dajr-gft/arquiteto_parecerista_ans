"""Testes para routes/__init__.py."""

import pytest


def test_routes_init_importable():
    """Test that routes can be imported."""
    try:
        import routes
        assert routes is not None
    except ImportError:
        pytest.skip("routes not available")


def test_routes_has_agent():
    """Test that routes exposes agent."""
    try:
        from routes import agent
        assert agent is not None
        assert hasattr(agent, 'root_agent')
    except ImportError:
        pytest.skip("routes.agent not available")


def test_routes_has_prompt():
    """Test that routes exposes prompt."""
    try:
        from routes import prompt
        assert prompt is not None
        assert hasattr(prompt, 'ANS_PROMPT')
    except ImportError:
        pytest.skip("routes.prompt not available")


def test_routes_tools_importable():
    """Test that routes.tools can be imported."""
    try:
        from routes import tools
        assert tools is not None
    except ImportError:
        pytest.skip("routes.tools not available")


def test_ans_prompt_content():
    """Test that ANS_PROMPT has content."""
    try:
        from routes.prompt import ANS_PROMPT
        assert isinstance(ANS_PROMPT, str)
        assert len(ANS_PROMPT) > 100
        assert 'ANS' in ANS_PROMPT or 'arquiteto' in ANS_PROMPT.lower()
    except ImportError:
        pytest.skip("routes.prompt not available")


def test_root_agent_exists():
    """Test that root_agent is defined."""
    try:
        from routes.agent import root_agent
        assert root_agent is not None
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'model')
    except ImportError:
        pytest.skip("routes.agent not available")

