import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module

@pytest.fixture
def client():
    """Provide a TestClient and restore the in-memory activities after each test."""
    backup = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    yield client
    # restore original state
    app_module.activities = backup
