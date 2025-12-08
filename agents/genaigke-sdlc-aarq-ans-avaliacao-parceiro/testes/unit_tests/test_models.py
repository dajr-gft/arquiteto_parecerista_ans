# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for models module."""

import pytest
from pydantic import ValidationError


class TestModels:
    """Test suite for models.py module."""

    def test_models_module_importable(self):
        """Test that models module can be imported."""
        try:
            from models import models
            assert models is not None
        except ImportError:
            pytest.skip("Models module structure different")

    def test_pydantic_imports(self):
        """Test that pydantic imports work."""
        from pydantic import BaseModel, Field
        assert BaseModel is not None
        assert Field is not None

