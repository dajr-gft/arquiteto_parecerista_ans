"""Testes adicionais para routes/agent.py para alcançar 85%."""

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.mark.asyncio
async def test_agent_with_image_file():
    """Test agent with image file."""
    with patch('routes.agent.InMemorySessionService') as mock_sess, \
         patch('routes.agent.InMemoryMemoryService') as mock_mem, \
         patch('routes.agent.Runner') as mock_runner, \
         patch('routes.agent.validate_file_security'), \
         patch('routes.agent.log_request_audit'), \
         patch('routes.agent.log_response_audit'):

        sess = Mock()
        sess.create_session = AsyncMock()
        mock_sess.return_value = sess

        mem = Mock()
        mock_mem.return_value = mem

        runner = Mock()
        event = Mock()
        event.is_final_response.return_value = True
        content = Mock()
        part = Mock()
        part.text = "Image analyzed"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        from genai_framework.models import FileInput
        file = FileInput("image.png", b"\x89PNG")

        from routes.agent import agent
        result = await agent(text=None, files=[file])
        assert result == "Image analyzed"


@pytest.mark.asyncio
async def test_agent_with_multiple_files():
    """Test agent with multiple files."""
    with patch('routes.agent.InMemorySessionService') as mock_sess, \
         patch('routes.agent.InMemoryMemoryService') as mock_mem, \
         patch('routes.agent.Runner') as mock_runner, \
         patch('routes.agent.validate_file_security'), \
         patch('routes.agent.validate_files_count'), \
         patch('routes.agent.log_request_audit'), \
         patch('routes.agent.log_response_audit'):

        sess = Mock()
        sess.create_session = AsyncMock()
        mock_sess.return_value = sess

        mem = Mock()
        mock_mem.return_value = mem

        runner = Mock()
        event = Mock()
        event.is_final_response.return_value = True
        content = Mock()
        part = Mock()
        part.text = "Multiple files processed"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        from genai_framework.models import FileInput
        files = [
            FileInput("doc1.txt", b"content1"),
            FileInput("doc2.txt", b"content2")
        ]

        from routes.agent import agent
        result = await agent(text=None, files=files)
        assert result == "Multiple files processed"


@pytest.mark.asyncio
async def test_agent_with_text_and_files():
    """Test agent with both text and files."""
    with patch('routes.agent.InMemorySessionService') as mock_sess, \
         patch('routes.agent.InMemoryMemoryService') as mock_mem, \
         patch('routes.agent.Runner') as mock_runner, \
         patch('routes.agent.validate_file_security'), \
         patch('routes.agent.log_request_audit'), \
         patch('routes.agent.log_response_audit'):

        sess = Mock()
        sess.create_session = AsyncMock()
        mock_sess.return_value = sess

        mem = Mock()
        mock_mem.return_value = mem

        runner = Mock()
        event = Mock()
        event.is_final_response.return_value = True
        content = Mock()
        part = Mock()
        part.text = "Text and file processed"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        from genai_framework.models import FileInput
        file = FileInput("doc.txt", b"content")

        from routes.agent import agent
        result = await agent(text="Analyze this", files=[file])
        assert result == "Text and file processed"


@pytest.mark.asyncio
async def test_ans_review_with_files():
    """Test ans_review endpoint with files."""
    with patch('routes.agent.agent') as mock_agent:
        mock_agent.return_value = "File result"

        from genai_framework.models import FileInput
        files = [FileInput("test.txt", b"content")]

        from routes.agent import ans_review
        result = await ans_review(texto=None, files=files)
        assert result == {"response": "File result"}


def test_validate_environment_raises_error_with_missing_vars():
    """Test environment validation raises error with missing variables."""
    with patch.dict(os.environ, {
        'GOOGLE_CLOUD_PROJECT': 'test-project'
        # Missing other required vars
    }, clear=True):
        from routes.agent import validate_environment_variables
        # Should raise ValueError with missing vars
        with pytest.raises(ValueError):
            validate_environment_variables()


def test_root_agent_attributes():
    """Test root_agent has required attributes."""
    from routes.agent import root_agent

    assert hasattr(root_agent, 'name')
    assert hasattr(root_agent, 'model')
    assert hasattr(root_agent, 'description')
    assert hasattr(root_agent, 'instruction')

