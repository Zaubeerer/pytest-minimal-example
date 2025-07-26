import pytest


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
