import pytest

# Global counter to track autouse fixture calls
_autouse_call_count = 0


@pytest.fixture(scope="session")
def test_session_data():
    """Session-scoped fixture that provides shared data for the entire test session."""
    print("\nSetting up session-scoped fixture")
    session_config = {
        "test_run_id": "pytest-minimal-example-session",
        "environment": "test",
        "start_time": "2025-07-26",
        "shared_counter": 0,
        "autouse_calls": 0,  # Track autouse calls in session data
    }
    yield session_config
    print(
        f"\nTearing down session-scoped fixture - autouse was called {session_config['autouse_calls']} times"
    )


@pytest.fixture(autouse=True)
def auto_setup_teardown(test_session_data):
    """Autouse fixture that runs before and after each test automatically."""
    global _autouse_call_count
    _autouse_call_count += 1
    test_session_data["autouse_calls"] += 1

    print(f"\n[AUTO] Setting up before test (call #{_autouse_call_count})")
    yield  # yield can be used to run teardown code after the fixture usage in a test
    print(f"\n[AUTO] Cleaning up after test (call #{_autouse_call_count})")


@pytest.fixture(
    params=[
        pytest.param(10, id="base_value_10"),
        pytest.param(5, id="base_value_5"),
        pytest.param(0, id="base_value_zero"),
        pytest.param(-3, id="base_value_negative", marks=pytest.mark.negative),
    ]
)
def base_number(request):
    """Parametrized fixture providing base numbers for testing."""
    return request.param
