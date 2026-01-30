# Quick Start Guide

Get up and running with uPlot Playground in under 2 minutes.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed

Install uv if you haven't:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
cd uplot-playground
uv sync
```

## Run the Application

```bash
uv run uvicorn main:app --reload
```

Open your browser to: **http://localhost:8000**

## What You'll See

Six interactive chart demonstrations:

1. **Line Chart** - Multi-series time series data
2. **Bar Chart** - Monthly sales data
3. **Real-time Chart** - Click "Start" to see live updates
4. **Multi-Axis Chart** - Temperature and pressure on different scales
5. **Area Chart** - System resource usage
6. **Scatter Plot** - Correlation visualization

## Try the API

```bash
curl http://localhost:8000/api/timeseries
curl http://localhost:8000/api/bars
curl http://localhost:8000/api/realtime
```

## Next Steps

- Edit `main.py` to modify data generation
- Customize charts in `static/js/charts.js`
- Update styles in `static/css/styles.css`
- Add new chart types following the existing patterns

## Common Commands

```bash
uv add package-name        # Add a dependency
uv remove package-name     # Remove a dependency
uv sync                    # Update dependencies
uv pip list                # List installed packages
uv run python script.py    # Run Python scripts
```

## Troubleshooting

**Port already in use?**
```bash
lsof -ti:8000 | xargs kill
```

**Dependencies not installing?**
```bash
rm -rf .venv uv.lock
uv sync
```

**Charts not rendering?**
- Check browser console (F12)
- Verify API endpoints return data
- Ensure uPlot CDN is accessible

## Learn More

- Read `claude.md` for detailed project context
- Check `README.md` for comprehensive documentation
- Visit [uPlot docs](https://github.com/leeoniya/uPlot) for chart options
