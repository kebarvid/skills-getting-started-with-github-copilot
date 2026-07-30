from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


_BASELINE_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory data before each test to keep tests independent."""
    activities.clear()
    activities.update(deepcopy(_BASELINE_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)