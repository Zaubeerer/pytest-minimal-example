import pytest
from contextlib import nullcontext

from main import get_the_value


@pytest.mark.parametrize(
    "data, key, expected_behaviour",
    [
        pytest.param(
            {"a": 1, "b": 2},
            "a",
            nullcontext(1), # You can also pass expected value directly here.
            id="key_a_exists"),
        pytest.param(
            {"x": 10, "y": 20},
            "y",
            nullcontext(20),
            id="key_y_exists"),
        pytest.param(
            {"name": "Alice", "age": 30},
            "name",
            nullcontext("Alice"),
            id="key_name_exists"),
        pytest.param(
            {"foo": "bar"},
            "baz",
            pytest.raises(KeyError, match="Key 'baz' not found in data"),
            id="key_baz_does_not_exist"),
    ],
)
def test_get_the_value(data, key, expected_behaviour):
    with expected_behaviour as value:
        result = get_the_value(data, key)
        assert result == value