import pytest
from hypothesis import given, strategies as st, assume, example, settings, note
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from lib import sum_objects


class TestSumObjectsWithHypothesis:
    """Test class demonstrating various Hypothesis features for testing sum_objects."""

    @given(st.integers(), st.integers())
    def test_sum_integers_property(self, a, b):
        """Property-based test: sum of integers should always be commutative."""
        result1 = sum_objects(a, b)
        result2 = sum_objects(b, a)
        assert result1 == result2, (
            f"Commutative property failed: {a} + {b} != {b} + {a}"
        )

    @given(st.integers(), st.integers(), st.integers())
    def test_sum_associative_property(self, a, b, c):
        """Property-based test: sum should be associative."""
        result1 = sum_objects(sum_objects(a, b), c)
        result2 = sum_objects(a, sum_objects(b, c))
        assert result1 == result2, (
            f"Associative property failed: ({a} + {b}) + {c} != {a} + ({b} + {c})"
        )

    @given(st.integers())
    def test_sum_identity_property(self, a):
        """Property-based test: adding zero should return the original number."""
        assert sum_objects(a, 0) == a
        assert sum_objects(0, a) == a

    @given(
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False),
    )
    def test_sum_floats_property(self, a, b):
        """Property-based test for float addition with constraints."""
        # Skip very large numbers that might cause overflow
        assume(abs(a) < 1e10 and abs(b) < 1e10)

        result = sum_objects(a, b)

        # Property: result should be approximately equal to a + b
        expected = a + b
        assert abs(result - expected) < 1e-10, (
            f"Float addition failed: {a} + {b} = {result}, expected {expected}"
        )

    @given(st.text(), st.text())
    def test_sum_strings_property(self, a, b):
        """Property-based test for string concatenation."""
        result = sum_objects(a, b)

        # Properties of string concatenation
        assert isinstance(result, str)
        assert len(result) == len(a) + len(b)
        assert result.startswith(a)
        assert result.endswith(b)

    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_sum_lists_property(self, a, b):
        """Property-based test for list concatenation."""
        result = sum_objects(a, b)

        # Properties of list concatenation
        assert isinstance(result, list)
        assert len(result) == len(a) + len(b)
        assert result[: len(a)] == a
        assert result[len(a) :] == b

    @given(st.one_of(st.integers(), st.floats(allow_nan=False)), st.text())
    def test_sum_incompatible_types_raises_error(self, number, text):
        """Property-based test: incompatible types should raise TypeError."""
        assume(text != "")  # Avoid empty strings which might have special behavior

        with pytest.raises(TypeError):
            sum_objects(number, text)

        with pytest.raises(TypeError):
            sum_objects(text, number)

    @given(st.integers(min_value=-1000, max_value=1000))
    @example(0)  # Always test the edge case of zero
    @example(1)  # Always test the edge case of one
    @example(-1)  # Always test the edge case of negative one
    def test_sum_with_explicit_examples(self, x):
        """Hypothesis test with explicit examples that always run."""
        result = sum_objects(x, x)
        assert result == 2 * x

    @given(st.integers())
    @settings(max_examples=200, deadline=None)
    def test_sum_with_custom_settings(self, x):
        """Test with custom Hypothesis settings."""
        # Use note() to add information to the test output
        note(f"Testing with value: {x}")

        result = sum_objects(x, -x)
        assert result == 0, f"Sum of {x} and {-x} should be 0, got {result}"

    @given(st.data())
    def test_sum_with_data_strategy(self, data):
        """Test using st.data() for more complex test generation."""
        # Generate a base number
        base = data.draw(st.integers(min_value=-100, max_value=100))

        # Generate an offset based on the base
        if base > 0:
            offset = data.draw(st.integers(min_value=-base, max_value=100))
        else:
            offset = data.draw(st.integers(min_value=-100, max_value=-base))

        # Test that sum is correct
        result = sum_objects(base, offset)
        expected = base + offset
        assert result == expected


# Composite strategy example
@st.composite
def number_and_small_offset(draw):
    """Composite strategy that generates a number and a small offset."""
    base = draw(st.integers(min_value=-100, max_value=100))
    offset = draw(st.integers(min_value=-10, max_value=10))
    return base, offset


class TestAdvancedHypothesis:
    """Advanced Hypothesis testing features."""

    @given(number_and_small_offset())
    def test_sum_with_composite_strategy(self, number_offset_pair):
        """Test using a composite strategy to generate related test data."""
        base, offset = number_offset_pair

        # Test that sum is correct
        result = sum_objects(base, offset)
        expected = base + offset
        assert result == expected

    @given(st.lists(st.integers(), min_size=1, max_size=10))
    def test_sum_multiple_numbers(self, numbers):
        """Test summing multiple numbers using reduce-like approach."""
        # Start with first number
        result = numbers[0]

        # Add each subsequent number
        for num in numbers[1:]:
            result = sum_objects(result, num)

        # Should equal the built-in sum
        expected = sum(numbers)
        assert result == expected

    @given(st.dictionaries(st.text(min_size=1, max_size=5), st.integers(), min_size=1))
    def test_sum_dict_values(self, test_dict):
        """Test summing dictionary values."""
        values = list(test_dict.values())

        if len(values) == 1:
            result = values[0]
        else:
            result = values[0]
            for value in values[1:]:
                result = sum_objects(result, value)

        expected = sum(values)
        assert result == expected

    @given(
        st.recursive(
            st.integers(),
            lambda children: st.lists(children, min_size=1, max_size=3),
            max_leaves=10,
        )
    )
    def test_sum_nested_structure(self, nested_data):
        """Test with recursively generated nested data structures."""

        def flatten_and_sum(data):
            if isinstance(data, int):
                return data
            elif isinstance(data, list):
                total = 0
                for item in data:
                    total = sum_objects(total, flatten_and_sum(item))
                return total
            return 0

        result = flatten_and_sum(nested_data)

        # Flatten manually for comparison
        def flatten(data):
            if isinstance(data, int):
                return [data]
            elif isinstance(data, list):
                result = []
                for item in data:
                    flattened = flatten(item)
                    if flattened is not None:
                        result.extend(flattened)
                return result
            return []

        flattened = flatten(nested_data)
        expected = sum(flattened) if flattened else 0
        assert result == expected


class CalculatorStateMachine(RuleBasedStateMachine):
    """Stateful testing example using Hypothesis."""

    def __init__(self):
        super().__init__()
        self.total = 0
        self.operations = []

    @rule(value=st.integers(min_value=-1000, max_value=1000))
    def add_number(self, value):
        """Rule: add a number to the total."""
        old_total = self.total
        self.total = sum_objects(self.total, value)
        self.operations.append(f"add({value})")

        # Verify the operation
        assert self.total == old_total + value

    @rule(value=st.integers(min_value=-1000, max_value=1000))
    def subtract_number(self, value):
        """Rule: subtract a number from the total."""
        old_total = self.total
        self.total = sum_objects(self.total, -value)
        self.operations.append(f"subtract({value})")

        # Verify the operation
        assert self.total == old_total - value

    @invariant()
    def total_is_integer(self):
        """Invariant: total should always be an integer."""
        assert isinstance(self.total, int)

    @invariant()
    def operations_recorded(self):
        """Invariant: we should have recorded our operations."""
        # This is a simple invariant - we should always have operations if total != 0
        if self.total == 0 and len(self.operations) > 0:
            # If we're back to 0, we should have had some operations
            pass  # This is fine


# Create the stateful test
TestCalculatorStateMachine = CalculatorStateMachine.TestCase


@pytest.mark.hypothesis
class TestHypothesisIntegration:
    """Tests demonstrating Hypothesis integration with pytest features."""

    @given(st.integers())
    @pytest.mark.parametrize("multiplier", [1, 2, 3])
    def test_hypothesis_with_parametrize(self, multiplier, value):
        """Combining Hypothesis with pytest.mark.parametrize."""
        result = sum_objects(value, value * (multiplier - 1))
        expected = value * multiplier
        assert result == expected

    @given(st.integers())
    def test_hypothesis_with_fixture(self, value, test_session_data):
        """Using Hypothesis with pytest fixtures."""
        # Access session data from our fixture
        assert "test_run_id" in test_session_data

        # Increment our session counter for each hypothesis example
        test_session_data["shared_counter"] += 1

        # Test the actual functionality
        result = sum_objects(value, 1)
        assert result == value + 1

    @given(st.integers())
    @pytest.mark.xfail(reason="Demonstrating xfail with Hypothesis")
    def test_hypothesis_with_xfail(self, value):
        """Showing how xfail works with Hypothesis."""
        # This will fail because we're asserting something incorrect
        result = sum_objects(value, 1)
        assert result == value  # This is wrong, should be value + 1


if __name__ == "__main__":
    # Example of running Hypothesis directly
    from hypothesis import given, strategies as st

    @given(st.integers(), st.integers())
    def test_example(a, b):
        assert sum_objects(a, b) == sum_objects(b, a)

    # This would run the test directly
    # test_example()
    pass
