"""Testes para genai_framework/decorators.py - Aumentar cobertura para 85%+."""

import pytest
from unittest.mock import Mock


class TestPostRoute:
    """Testes para decorator post_route."""

    def test_post_route_without_name(self):
        """Test post_route decorator without route name."""
        from genai_framework.decorators import post_route

        @post_route
        def test_func():
            return "result"

        assert callable(test_func)
        assert test_func() == "result"
        assert test_func._route_type == 'POST'
        assert test_func._route_name == 'test_func'

    def test_post_route_with_name(self):
        """Test post_route decorator with custom route name."""
        from genai_framework.decorators import post_route

        @post_route("custom_route")
        def test_func():
            return "result"

        assert callable(test_func)
        assert test_func() == "result"
        assert test_func._route_type == 'POST'
        assert test_func._route_name == "custom_route"

    def test_post_route_with_args(self):
        """Test post_route decorated function with arguments."""
        from genai_framework.decorators import post_route

        @post_route
        def test_func(a, b):
            return a + b

        result = test_func(1, 2)
        assert result == 3

    def test_post_route_with_kwargs(self):
        """Test post_route decorated function with keyword arguments."""
        from genai_framework.decorators import post_route

        @post_route
        def test_func(a=1, b=2):
            return a + b

        result = test_func(a=5, b=10)
        assert result == 15


class TestGetRoute:
    """Testes para decorator get_route."""

    def test_get_route_without_name(self):
        """Test get_route decorator without route name."""
        from genai_framework.decorators import get_route

        @get_route
        def test_func():
            return "result"

        assert callable(test_func)
        assert test_func() == "result"
        assert test_func._route_type == 'GET'
        assert test_func._route_name == 'test_func'

    def test_get_route_with_name(self):
        """Test get_route decorator with custom route name."""
        from genai_framework.decorators import get_route

        @get_route("custom_get")
        def test_func():
            return "result"

        assert callable(test_func)
        assert test_func() == "result"
        assert test_func._route_type == 'GET'
        assert test_func._route_name == "custom_get"

    def test_get_route_with_args(self):
        """Test get_route decorated function with arguments."""
        from genai_framework.decorators import get_route

        @get_route
        def test_func(a, b):
            return a * b

        result = test_func(3, 4)
        assert result == 12


class TestFileInputRoute:
    """Testes para decorator file_input_route."""

    def test_file_input_route_without_name(self):
        """Test file_input_route decorator without route name."""
        from genai_framework.decorators import file_input_route

        @file_input_route
        def test_func(file):
            return f"Processing {file}"

        assert callable(test_func)
        result = test_func("test.pdf")
        assert result == "Processing test.pdf"
        assert test_func._route_type == 'POST'  # file_input_route uses POST
        assert test_func._route_name == 'test_func'
        assert test_func._accepts_file is True

    def test_file_input_route_with_name(self):
        """Test file_input_route decorator with custom route name."""
        from genai_framework.decorators import file_input_route

        @file_input_route("upload_file")
        def test_func(file):
            return f"Uploaded {file}"

        assert callable(test_func)
        result = test_func("doc.txt")
        assert result == "Uploaded doc.txt"
        assert test_func._route_type == 'POST'  # file_input_route uses POST
        assert test_func._route_name == "upload_file"
        assert test_func._accepts_file is True

    def test_file_input_route_with_mock_file(self):
        """Test file_input_route with mock file object."""
        from genai_framework.decorators import file_input_route

        @file_input_route
        def process_file(file):
            return file.filename if hasattr(file, 'filename') else str(file)

        mock_file = Mock()
        mock_file.filename = "test.pdf"

        result = process_file(mock_file)
        assert result == "test.pdf"


class TestDecoratorsIntegration:
    """Testes de integração para decorators."""

    def test_multiple_decorators(self):
        """Test function with multiple route types metadata."""
        from genai_framework.decorators import post_route

        @post_route("multi_route")
        def test_func(data):
            return {"processed": data}

        result = test_func({"input": "test"})
        assert result == {"processed": {"input": "test"}}
        assert hasattr(test_func, '_route_type')
        assert hasattr(test_func, '_route_name')

    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves original function name."""
        from genai_framework.decorators import post_route

        @post_route
        def my_function():
            pass

        assert my_function.__name__ == 'my_function'

    def test_decorator_preserves_docstring(self):
        """Test that decorator preserves function docstring."""
        from genai_framework.decorators import post_route

        @post_route
        def my_function():
            """This is a docstring."""
            pass

        assert my_function.__doc__ == """This is a docstring."""

    def test_all_decorators_available(self):
        """Test that all decorators can be imported."""
        from genai_framework import decorators

        assert hasattr(decorators, 'post_route')
        assert hasattr(decorators, 'get_route')
        assert hasattr(decorators, 'file_input_route')

        assert callable(decorators.post_route)
        assert callable(decorators.get_route)
        assert callable(decorators.file_input_route)

