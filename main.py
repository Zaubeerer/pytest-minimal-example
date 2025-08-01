import requests
from typing import Any


def main():
    print("Hello from pytest-minimal-example!")


def get_the_value(data: dict[str: Any], key: str) -> Any:
    """
    Retrieve the value associated with a key in a dictionary.

    A stupid function that instead of returning a default value None,
    raises an error.

    Parameters
    ----------
    data : dict[str, Any]
        The dictionary from which to retrieve the value.
    key : str
        The key whose value is to be retrieved.

    Returns
    -------
    Any
        The value associated with the key in the dictionary.
    """
    if not (value := data.get(key)):
        err = f"Key '{key}' not found in data"
        raise KeyError(err)
    return value


def get_my_public_api() -> str:
    """
    A public API function that returns a string.

    Returns
    -------
    str
        A string indicating the public API.
    """
    url = "https://api.ipify.org"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}, status code: {response.status_code}")
    return response.text


if __name__ == "__main__":
    main()
