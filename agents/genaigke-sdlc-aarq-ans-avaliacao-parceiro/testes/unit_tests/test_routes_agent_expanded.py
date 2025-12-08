"""Testes expandidos para routes/agent.py - Cobertura completa."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import os


@pytest.mark.asyncio
async def test_agent_with_text_only():
    """Test agent with text input only."""
    with patch('routes.agent.InMemorySessionService') as mock_sess, \
         patch('routes.agent.InMemoryMemoryService') as mock_mem, \
         patch('routes.agent.Runner') as mock_runner, \
         patch('routes.agent.log_request_audit'), \
         patch('routes.agent.log_response_audit'):

        # Setup mocks
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
        part.text = "Response"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        from routes.agent import agent
        result = await agent(text="Test", files=None)
        assert result == "Response"


@pytest.mark.asyncio
async def test_agent_with_pdf_file():
    """Test agent with PDF file."""
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
        part.text = "PDF processed"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        file = Mock()
        file.filename = "doc.pdf"
        file.content_type = "application/pdf"
        file.read = AsyncMock(return_value=b"%PDF")

        from routes.agent import agent
        result = await agent(text=None, files=[file])
        assert result == "PDF processed"


@pytest.mark.asyncio
async def test_agent_with_excel_file():
    """Test agent with Excel file."""
    with patch('routes.agent.InMemorySessionService') as mock_sess, \
         patch('routes.agent.InMemoryMemoryService') as mock_mem, \
         patch('routes.agent.Runner') as mock_runner, \
         patch('routes.agent.validate_file_security'), \
         patch('routes.agent.pd.read_excel') as mock_excel, \
         patch('routes.agent.log_request_audit'), \
         patch('routes.agent.log_response_audit'):

        df = Mock()
        df.to_csv.return_value = "col1,col2\nval1,val2"
        mock_excel.return_value = {"Sheet1": df}

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
        part.text = "Excel processed"
        content.parts = [part]
        event.content = content
        runner.run.return_value = [event]
        mock_runner.return_value = runner

        file = Mock()
        file.filename = "data.xlsx"
        file.content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file.read = AsyncMock(return_value=b"PK\x03\x04")

        from routes.agent import agent
        result = await agent(text=None, files=[file])
        assert result == "Excel processed"


@pytest.mark.asyncio
async def test_agent_no_content_error():
    """Test agent with no content raises error."""
    from routes.agent import agent
    with pytest.raises(ValueError):
        await agent(text=None, files=None)


@pytest.mark.asyncio
async def test_ans_review_success():
    """Test ans_review endpoint success."""
    with patch('routes.agent.agent') as mock_agent:
        mock_agent.return_value = "Result"

        from routes.agent import ans_review
        result = await ans_review(texto="Test", files=None)
        assert result == {"response": "Result"}


@pytest.mark.asyncio
async def test_ans_review_no_content():
    """Test ans_review with no content."""
    from routes.agent import ans_review
    result = await ans_review(texto=None, files=None)
    # ans_review returns tuple (dict, status_code) on error
    if isinstance(result, tuple):
        assert "error" in result[0]
        assert result[1] == 400
    else:
        assert "error" in result


@pytest.mark.asyncio
async def test_ans_review_value_error():
    """Test ans_review handles ValueError."""
    with patch('routes.agent.agent') as mock_agent:
        mock_agent.side_effect = ValueError("Error")

        from routes.agent import ans_review
        result = await ans_review(texto="Test", files=None)
        # ans_review returns tuple (dict, status_code) on error
        if isinstance(result, tuple):
            assert "error" in result[0]
            assert result[1] == 400
        else:
            assert "error" in result


@pytest.mark.asyncio
async def test_ans_review_generic_error():
    """Test ans_review handles generic error."""
    with patch('routes.agent.agent') as mock_agent:
        mock_agent.side_effect = Exception("Error")

        from routes.agent import ans_review
        result = await ans_review(texto="Test", files=None)
        # ans_review returns tuple (dict, status_code) on error
        if isinstance(result, tuple):
            assert "error" in result[0]
            assert result[1] == 500
        else:
            assert "error" in result


@pytest.mark.asyncio
async def test_health_check():
    """Test health_check endpoint."""
    from routes.agent import health_check
    result = await health_check()
    assert result["status"] == "healthy"
    assert "service" in result
    assert "timestamp" in result


def test_validate_environment_variables_success():
    """Test env vars validation success."""
    with patch.dict(os.environ, {
        'GOOGLE_CLOUD_PROJECT': 'test',
        'GOOGLE_CLOUD_LOCATION': 'us',
        'GOOGLE_GENAI_USE_VERTEXAI': 'True'
    }):
        from routes.agent import validate_environment_variables
        validate_environment_variables()


def test_validate_environment_variables_fail():
    """Test env vars validation fails."""
    with patch.dict(os.environ, {}, clear=True):
        from routes.agent import validate_environment_variables
        with pytest.raises(ValueError):
            validate_environment_variables()

