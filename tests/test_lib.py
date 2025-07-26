import pytest
from lib import sum_objects


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(1, 2, 3, id="positive_integers"),
        pytest.param(0, 0, 0, id="zeros"),
        pytest.param(-1, 1, 0, id="negative_positive"),
        pytest.param(1.5, 2.5, 4.0, id="floats"),
        pytest.param("hello", " world", "hello world", id="strings"),
        pytest.param([1, 2], [3, 4], [1, 2, 3, 4], id="lists"),
        pytest.param(
            1,
            2,
            4,
            id="expected_failure",
            marks=pytest.mark.xfail(reason="This should fail - 1+2 != 4", strict=True),
        ),  # this test should pass, because it is expected to fail and fails
        pytest.param(
            2,
            2,
            4,
            id="expected_failure",
            marks=pytest.mark.xfail(reason="This should fail - 1+2 != 4", strict=False),
        ),  # this test passes, although it is expected to fail, because strict=False
        pytest.param(
            2,
            2,
            4,
            id="expected_failure",
            marks=pytest.mark.xfail(reason="This should fail - 1+2 != 4", strict=True),
        ),  # this test should fail, because it is strictly expected to fail but passes
        pytest.param(
            100,
            200,
            300,
            id="large_numbers",
            marks=pytest.mark.skip(reason="Skipping large number test for demo"),
        ),
    ],
)
def test_sum_objects_parametrized(a, b, expected):
    """Test sum_objects function with various parameter combinations."""
    result = sum_objects(a, b)
    assert result == expected


@pytest.mark.parametrize(
    "a,b",
    [
        pytest.param(1.5, "a", id="float_with_string"),
        pytest.param("hello", 42, id="string_with_number"),
        pytest.param([1, 2], "test", id="list_with_string"),
        pytest.param(
            None,
            5,
            id="none_with_number",
            marks=pytest.mark.xfail(reason="None + number should raise TypeError"),
        ),
    ],
)
def test_sum_objects_type_errors(a, b):
    """Test that sum_objects raises TypeError for incompatible types."""
    with pytest.raises(TypeError):
        sum_objects(a, b)


def test_sum_with_fixture(base_number):
    """Test sum_objects using the parametrized fixture from conftest.py."""
    result = sum_objects(base_number, 1)
    assert result == base_number + 1


@pytest.mark.negative
def test_sum_negative_numbers():
    """Test specifically for negative numbers (uses mark from fixture)."""
    result = sum_objects(-5, -3)
    assert result == -8
