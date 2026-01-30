# Test Suite Documentation

## Overview

This directory contains the test suite for the uPlot Playground project. We use **pytest** as the testing framework with modern best practices.

## Test Structure

```
tests/
├── __init__.py           # Package marker
├── conftest.py           # Shared fixtures and pytest configuration
├── test_windowing.py     # Core windowing behavior tests
└── test_api.py          # FastAPI endpoint integration tests
```

## Test Categories

### Unit Tests (`test_windowing.py`)
Tests the core windowing logic that's implemented in JavaScript. The Python implementation mirrors the JS behavior for testing purposes.

**Test Classes:**
- `TestInitialState` - Default/initial behavior
- `TestClickBehavior` - Click-to-center window functionality
- `TestSliderBehavior` - Window size adjustment
- `TestResetBehavior` - Reset functionality
- `TestComplexScenarios` - Multi-step user interactions
- `TestEdgeCases` - Boundary conditions

**Total:** 33 tests

### Integration Tests (`test_api.py`)
Tests FastAPI endpoints and data quality.

**Test Classes:**
- `TestAPIEndpoints` - HTTP endpoint responses
- `TestDataQuality` - Data structure validation
- `TestErrorHandling` - Error cases and 404s

**Total:** 15 tests

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific file
uv run pytest tests/test_windowing.py

# Run specific class
uv run pytest tests/test_windowing.py::TestClickBehavior

# Run specific test
uv run pytest tests/test_windowing.py::TestClickBehavior::test_first_click_centers_window
```

### Coverage

```bash
# Run with coverage
uv run pytest --cov=.

# Detailed coverage with missing lines
uv run pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=. --cov-report=html
# Then open: htmlcov/index.html
```

### Test Markers

Tests can be marked for selective execution:

```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Exclude slow tests
uv run pytest -m "not slow"
```

## Writing New Tests

### Basic Test Structure

```python
def test_something():
    """Test description"""
    # Arrange
    expected = 42
    
    # Act
    result = some_function()
    
    # Assert
    assert result == expected
```

### Using Fixtures

Fixtures are defined in `conftest.py` and available to all tests:

```python
def test_with_fixture(windowing_simulator):
    """Use pre-configured fixtures"""
    result = windowing_simulator.get_windowed_data()
    assert result is not None
```

### Test Classes

Organize related tests in classes:

```python
class TestMyFeature:
    """Test suite for my feature"""
    
    def test_case_1(self):
        """First test case"""
        assert True
    
    def test_case_2(self):
        """Second test case"""
        assert True
```

### Parametrized Tests

Test multiple scenarios with one function:

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    """Test doubling function"""
    assert input * 2 == expected
```

### API Testing

Use FastAPI TestClient for endpoint tests:

```python
def test_endpoint(client):
    """Test API endpoint"""
    response = client.get("/api/signal")
    assert response.status_code == 200
    assert "data" in response.json()
```

## Best Practices

### 1. Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Be descriptive: `test_click_centers_window` not `test_1`

### 2. Test Organization
- Group related tests in classes
- One assertion per test (when possible)
- Test one thing at a time
- Use fixtures for common setup

### 3. Test Documentation
- Write clear docstrings
- Explain **what** is being tested
- Include expected behavior

### 4. Assertions
```python
# Good
assert result == expected

# Better (with message)
assert result == expected, f"Expected {expected}, got {result}"

# Best (use pytest helpers)
assert result == pytest.approx(expected, abs=0.01)
```

### 5. Test Data
- Use fixtures for reusable test data
- Keep test data simple and focused
- Avoid hardcoding magic numbers

## Continuous Integration

When setting up CI/CD, use:

```yaml
# Example GitHub Actions
- name: Run tests
  run: uv run pytest --cov=. --cov-report=xml
  
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests fail locally but pass in CI
- Check Python version matches
- Ensure all dependencies installed: `uv sync`
- Clear pytest cache: `rm -rf .pytest_cache`

### Import errors
- Ensure you're in project root
- Run tests via `uv run pytest` not `python -m pytest`
- Check `__init__.py` files exist

### Fixture not found
- Check fixture is in `conftest.py`
- Ensure fixture name matches parameter name
- Verify `conftest.py` is in correct location

## Test Metrics

Current project status:
- **Total Tests:** 48
- **Coverage:** 100% on `main.py`
- **Pass Rate:** 100%
- **Avg Runtime:** ~1 second

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
