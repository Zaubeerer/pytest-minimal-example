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


if __name__ == "__main__":
    main()
