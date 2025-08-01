import pytest
from contextlib import nullcontext

from requests import Response

from main import get_the_value, get_my_public_api


@pytest.mark.parametrize(
    ("data", "key", "expected_behaviour"),
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


@pytest.mark.parametrize(
    ("status_code", "expected_behaviour"),
    [
        pytest.param(
            200, nullcontext()
        ),
        pytest.param(
            404, pytest.raises(
                Exception,
                match="Failed to fetch data from https://api.ipify.org, status code: 404"
        ))
    ]
)
def test_get_my_public_api(mocker, status_code, expected_behaviour):
    """
    Test the public API function to ensure it returns a string.
    """
    # Arrange
    expected_ip = "92.105.16.38"
    response = Response()
    response.status_code = status_code
    response._content = expected_ip.encode("utf-8")
    mocker.patch("requests.get", return_value=response)

    # Act & Assert
    with expected_behaviour:
        ip = get_my_public_api()
        assert ip == expected_ip