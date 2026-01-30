# uPlot Playground

A demonstration project showcasing [uPlot](https://github.com/leeoniya/uPlot) - a fast, memory-efficient charting library - with a Python backend using FastAPI.

## Features

This project demonstrates several uPlot use cases:

- **Line Charts**: Time series data with multiple series
- **Bar Charts**: Categorical data visualization
- **Real-time Updates**: Live data streaming
- **Interactive Features**: Zooming, panning, and tooltips
- **Multiple Y-Axes**: Different scales on the same chart
- **Area Charts**: Filled line charts

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Vanilla JavaScript with uPlot
- **Package Management**: uv (fast Python package installer)
- **Charts**: uPlot v1.6.x

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) installed

## Installation

1. Clone this repository
2. Install dependencies using uv:

```bash
uv sync
```

## Running the Application

Start the development server:

```bash
uv run uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Project Structure

```
uplot-playground/
├── main.py                 # FastAPI backend
├── static/                 # Static files (JS, CSS)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── charts.js
├── templates/              # HTML templates
│   └── index.html
├── data/                   # Sample data generators
│   └── generators.py
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── README.md               # This file
└── claude.md               # AI context documentation
```

## API Endpoints

- `GET /` - Main page with chart examples
- `GET /api/timeseries` - Time series data
- `GET /api/bars` - Bar chart data
- `GET /api/realtime` - Real-time streaming data
- `GET /api/multi-axis` - Multi-axis chart data

## uPlot Examples

### 1. Basic Line Chart
Simple time series visualization with single or multiple series.

### 2. Bar Chart
Categorical data with custom styling.

### 3. Real-time Chart
Live updating chart with streaming data.

### 4. Multi-Axis Chart
Multiple Y-axes for different data scales.

### 5. Area Chart
Filled area under line chart.

## Testing

Modern, comprehensive test suite following industry best practices.

### Backend Tests (Python + pytest)

**48 tests, 100% coverage** on backend code

```bash
# Run all backend tests
uv run pytest

# With coverage
uv run pytest --cov=. --cov-report=term-missing

# Specific tests
uv run pytest tests/test_windowing.py
uv run pytest tests/test_api.py
```

### Frontend Tests (E2E + Playwright)

**12 tests, 75% pass rate** for browser automation

```bash
# Run E2E tests
npm test

# Interactive UI mode
npm run test:ui

# Debug mode
npm run test:debug

# View test report
npm run test:report
```

### Quick Test All

```bash
# Backend + Frontend
make test && npm test

# Or separately
uv run pytest  # Backend
npm test       # Frontend E2E
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Pytest fixtures and configuration
├── test_windowing.py     # Windowing behavior tests (33 tests)
└── test_api.py          # FastAPI endpoint tests (15 tests)
```

### Test Coverage

- **48 tests total**, all passing
- **100% coverage** on `main.py`
- Tests include:
  - Initial state behavior
  - Click-to-center functionality
  - Slider adjustments
  - Reset behavior
  - Complex multi-step scenarios
  - Edge cases
  - API endpoint validation
  - Data quality checks

### Writing Tests

Add new tests to `tests/` directory following pytest conventions:
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

Use fixtures from `conftest.py` for common test data.

## Development

### Adding New Chart Types

1. Add data generator in `main.py`
2. Create API endpoint
3. Add chart configuration in `static/js/charts.js`
4. Update HTML template if needed
5. Write tests in `tests/test_api.py`

### Using uv Commands

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency (like testing tools)
uv add --dev package-name

# Run Python scripts
uv run python script.py

# Update dependencies
uv sync

# Show installed packages
uv pip list
```

## Resources

- [uPlot Documentation](https://github.com/leeoniya/uPlot)
- [uPlot Demos](https://leeoniya.github.io/uPlot/demos/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [uv Documentation](https://github.com/astral-sh/uv)

## License

MIT
