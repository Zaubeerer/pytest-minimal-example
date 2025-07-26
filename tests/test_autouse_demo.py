import pytest
from lib import sum_objects


@pytest.fixture(autouse=True, scope="function")
def file_specific_autouse():
    """Autouse fixture that only applies to tests in this file."""
    print("\n[FILE-AUTO] File-specific autouse fixture running")
    yield
    print("\n[FILE-AUTO] File-specific autouse fixture cleanup")


class TestClassWithAutouse:
    """Test class to demonstrate class-scoped autouse fixtures."""

    @pytest.fixture(autouse=True)
    def class_autouse(self):
        """Autouse fixture that only applies to tests in this class."""
        print("\n[CLASS-AUTO] Class-specific autouse fixture running")
        yield
        print("\n[CLASS-AUTO] Class-specific autouse fixture cleanup")

    def test_in_class_with_autouse(self):
        """Test inside class - should see both global, file, and class autouse fixtures."""
        result = sum_objects(10, 20)
        assert result == 30
        print("\nThis test is in a class with its own autouse fixture")

    def test_another_in_class(self):
        """Another test in the same class."""
        result = sum_objects(5, 15)
        assert result == 20


def test_outside_class():
    """Test outside the class - should see global and file autouse, but not class autouse."""
    result = sum_objects(1, 2)
    assert result == 3
    print("\nThis test is outside the class")


def test_check_autouse_with_request_fixture(request):
    """Test that shows how to inspect fixtures using the request fixture."""
    print(f"\nActive fixtures for this test: {list(request.fixturenames)}")

    # Check if our autouse fixtures are in the fixture names
    assert "auto_setup_teardown" in request.fixturenames, (
        "Global autouse fixture should be active"
    )
    assert "file_specific_autouse" in request.fixturenames, (
        "File autouse fixture should be active"
    )

    result = sum_objects(3, 7)
    assert result == 10
