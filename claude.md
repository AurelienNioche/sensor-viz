# Claude Context - uPlot Signal Processing Playground

## Project Overview

This is a signal processing visualization project showcasing uPlot's performance with real-time signal analysis. It combines uPlot (fast JavaScript charting), FastAPI backend, NumPy for signal generation, and SciPy for advanced signal processing.

## Purpose

The main goals of this project are:
1. Demonstrate signal processing techniques (FFT, filtering, PSD)
2. Showcase uPlot's performance with high-frequency data
3. Provide signal visualization examples
4. Serve as a learning resource for signal analysis with Python/JavaScript

## Architecture

### Backend (Python + FastAPI)
- **Framework**: FastAPI for REST API endpoints
- **Package Manager**: uv for dependency management
- **Signal Processing**: NumPy for signal generation, SciPy for filtering/FFT/PSD
- **Data Generation**: Composite signals, noise, frequency components
- **Static Files**: Serves HTML, CSS, JS

### Frontend (Vanilla JS + uPlot + Plotly.js)
- **Chart Libraries**:
  - uPlot v1.6.x for 2D time-series (CDN)
  - Plotly.js v2.27.x for 3D visualizations (CDN)
- **No Framework**: Pure JavaScript for simplicity
- **Responsive**: Charts adapt to container size
- **Interactive**: Zoom, pan, tooltips, 3D rotation

## Key Files

### `main.py`
FastAPI application with signal processing endpoints:
- `/api/signal` - Time domain composite signal
- `/api/fft` - Frequency domain analysis (FFT)
- `/api/filtering` - Low-pass filter demonstration
- `/api/psd` - Power spectral density (Welch's method)
- `/api/bandpass` - Bandpass filter (isolating frequency bands)
- `/api/accelerometer` - 3D accelerometer data (simulated motion)

### `static/js/charts.js`
uPlot chart configurations for signal visualizations. Each function handles a specific signal processing visualization.

### `pyproject.toml`
Project configuration with dependencies: FastAPI, NumPy, SciPy, uvicorn.

## uPlot Integration

### Data Format
uPlot expects data in columnar format:
```javascript
[
  [timestamp1, timestamp2, ...],  // x-axis (time)
  [value1, value2, ...],           // series 1
  [value1, value2, ...]            // series 2
]
```

### Chart Configuration
Each chart requires:
- `width` and `height`
- `data` array
- `series` array (describes each line/bar)
- `axes` configuration
- Optional `scales` for custom ranges

### Performance
uPlot is chosen for its:
- Small bundle size (~45KB minified)
- Fast rendering (can handle millions of points)
- Low memory footprint
- Canvas-based rendering

## Development Guidelines

### Adding New Chart Types

1. **Backend**: Add data generator and API endpoint
2. **Frontend**: Create chart configuration in `charts.js`
3. **Testing**: Verify data format matches uPlot expectations
4. **Documentation**: Update README with new example

### Code Style

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use modern ES6+ features, clear variable names
- **Comments**: Only add comments for complex logic, not obvious code

### Dependencies

Core dependencies:
- **Backend**: FastAPI, uvicorn, NumPy, SciPy
- **Frontend**: uPlot from CDN (no npm/build step needed)

## Common Tasks

### Adding a Dependency
```bash
uv add package-name
```

### Running the Server
```bash
uv run uvicorn main:app --reload
```

### Testing Endpoints
```bash
curl http://localhost:8000/api/signal
curl http://localhost:8000/api/fft
curl http://localhost:8000/api/psd
```

## uPlot Best Practices

1. **Reuse Chart Instances**: Don't recreate charts on every update
2. **Use setData()**: Update existing charts rather than destroying/recreating
3. **Optimize Data**: Send only necessary precision (round to 2-3 decimals)
4. **Debounce Resize**: Handle window resize events efficiently
5. **Lazy Loading**: Create charts only when visible

## Troubleshooting

### Chart Not Rendering
- Check browser console for errors
- Verify data format (must be columnar arrays)
- Ensure uPlot CSS is loaded
- Check container has explicit width/height

### Data Not Loading
- Check FastAPI logs for endpoint errors
- Verify CORS settings
- Check network tab in browser DevTools
- Validate JSON structure

### Performance Issues
- Reduce data points (downsample)
- Use uPlot's built-in optimization options
- Consider using WebWorkers for data processing
- Check for memory leaks in update loops

## Signal Processing Features

### Implemented
- **Time Domain**: Composite signals with multiple frequency components
- **Frequency Domain**: FFT analysis with magnitude spectrum
- **Filtering**: Low-pass and bandpass filters
- **Spectral Analysis**: Power Spectral Density using Welch's method
- **3D Visualization**: Interactive 3D accelerometer trajectory with adjustable time window

### Future Enhancements
- Wavelet transforms
- Spectrogram (time-frequency visualization)
- IIR/FIR filter design tools
- Signal correlation and convolution
- Window functions comparison
- Phase analysis
- Audio signal processing examples

## Resources

- [uPlot GitHub](https://github.com/leeoniya/uPlot)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [NumPy FFT](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)
