from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import numpy as np

app = FastAPI(title="uPlot Playground - Signal Processing")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/signal")
async def get_signal():
    """Generate composite 3-channel signal in time domain"""
    sample_rate = 1000  # Hz
    duration = 2  # seconds
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Channel 1: Low frequency dominant (50Hz + harmonics)
    ch1 = (
        np.sin(2 * np.pi * 50 * t) +
        0.3 * np.sin(2 * np.pi * 150 * t) +
        0.1 * np.random.randn(n_samples)
    )

    # Channel 2: Mid frequency dominant (120Hz + harmonics)
    ch2 = (
        0.8 * np.sin(2 * np.pi * 120 * t) +
        0.4 * np.sin(2 * np.pi * 60 * t) +
        0.1 * np.random.randn(n_samples)
    )

    # Channel 3: High frequency dominant (200Hz + harmonics)
    ch3 = (
        0.6 * np.sin(2 * np.pi * 200 * t) +
        0.3 * np.sin(2 * np.pi * 100 * t) +
        0.1 * np.random.randn(n_samples)
    )

    # Downsample for plotting (every 2nd point)
    step = 2

    return {
        "data": {
            "time": t[::step].tolist(),
            "ch1": ch1[::step].tolist(),
            "ch2": ch2[::step].tolist(),
            "ch3": ch3[::step].tolist()
        },
        "sample_rate": sample_rate,
        "labels": ["Channel 1 (50Hz)", "Channel 2 (120Hz)", "Channel 3 (200Hz)"]
    }


@app.get("/api/fft")
async def get_fft():
    """Generate 3-channel FFT for frequency domain analysis"""
    sample_rate = 1000  # Hz
    duration = 2  # seconds
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Channel 1: Low frequency
    ch1_signal = np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 150 * t) + 0.1 * np.random.randn(n_samples)

    # Channel 2: Mid frequency
    ch2_signal = 0.8 * np.sin(2 * np.pi * 120 * t) + 0.4 * np.sin(2 * np.pi * 60 * t) + 0.1 * np.random.randn(n_samples)

    # Channel 3: High frequency
    ch3_signal = 0.6 * np.sin(2 * np.pi * 200 * t) + 0.3 * np.sin(2 * np.pi * 100 * t) + 0.1 * np.random.randn(n_samples)

    # Compute FFT for each channel
    def compute_fft(signal):
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(n_samples, 1/sample_rate)
        positive_mask = freqs >= 0
        return freqs[positive_mask], np.abs(fft[positive_mask])

    freqs, mag1 = compute_fft(ch1_signal)
    _, mag2 = compute_fft(ch2_signal)
    _, mag3 = compute_fft(ch3_signal)

    # Downsample for plotting
    step = 5

    return {
        "data": {
            "freq": freqs[::step].tolist(),
            "ch1": mag1[::step].tolist(),
            "ch2": mag2[::step].tolist(),
            "ch3": mag3[::step].tolist()
        },
        "labels": ["FFT Ch1 (50Hz)", "FFT Ch2 (120Hz)", "FFT Ch3 (200Hz)"],
        "sample_rate": sample_rate
    }


@app.get("/api/filtering")
async def get_filtering():
    """Generate 3-channel filtered signal"""
    sample_rate = 500  # Hz
    duration = 1  # second
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Channel 1: Low frequency signal + noise
    ch1_clean = np.sin(2 * np.pi * 10 * t)
    ch1_noise = 0.5 * np.sin(2 * np.pi * 150 * t) + 0.2 * np.random.randn(n_samples)
    ch1 = ch1_clean + ch1_noise

    # Channel 2: Mid frequency signal + noise
    ch2_clean = 0.8 * np.sin(2 * np.pi * 15 * t)
    ch2_noise = 0.4 * np.sin(2 * np.pi * 120 * t) + 0.2 * np.random.randn(n_samples)
    ch2 = ch2_clean + ch2_noise

    # Channel 3: Different frequency + noise
    ch3_clean = 0.6 * np.sin(2 * np.pi * 8 * t)
    ch3_noise = 0.3 * np.sin(2 * np.pi * 100 * t) + 0.2 * np.random.randn(n_samples)
    ch3 = ch3_clean + ch3_noise

    # Simple low-pass filter for each channel
    window_size = 15
    ch1_filtered = np.convolve(ch1, np.ones(window_size)/window_size, mode='same')
    ch2_filtered = np.convolve(ch2, np.ones(window_size)/window_size, mode='same')
    ch3_filtered = np.convolve(ch3, np.ones(window_size)/window_size, mode='same')

    # Downsample for plotting
    step = 2

    return {
        "data": {
            "time": t[::step].tolist(),
            "ch1": ch1_filtered[::step].tolist(),
            "ch2": ch2_filtered[::step].tolist(),
            "ch3": ch3_filtered[::step].tolist()
        },
        "labels": ["Filtered Ch1", "Filtered Ch2", "Filtered Ch3"],
        "sample_rate": sample_rate
    }


@app.get("/api/psd")
async def get_psd():
    """Generate 3-channel Power Spectral Density"""
    sample_rate = 1000  # Hz
    duration = 4  # seconds
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Channel 1: Low frequency components
    ch1 = 2.0 * np.sin(2 * np.pi * 50 * t) + 1.0 * np.sin(2 * np.pi * 150 * t) + 0.5 * np.random.randn(n_samples)

    # Channel 2: Mid frequency components
    ch2 = 1.5 * np.sin(2 * np.pi * 120 * t) + 0.8 * np.sin(2 * np.pi * 60 * t) + 0.5 * np.random.randn(n_samples)

    # Channel 3: High frequency components
    ch3 = 1.0 * np.sin(2 * np.pi * 200 * t) + 0.6 * np.sin(2 * np.pi * 100 * t) + 0.5 * np.random.randn(n_samples)

    # Compute Power Spectral Density using Welch's method for each channel
    from scipy import signal as scipy_signal
    freqs, psd1 = scipy_signal.welch(ch1, sample_rate, nperseg=1024)
    _, psd2 = scipy_signal.welch(ch2, sample_rate, nperseg=1024)
    _, psd3 = scipy_signal.welch(ch3, sample_rate, nperseg=1024)

    return {
        "data": {
            "freq": freqs.tolist(),
            "ch1": psd1.tolist(),
            "ch2": psd2.tolist(),
            "ch3": psd3.tolist()
        },
        "labels": ["PSD Ch1", "PSD Ch2", "PSD Ch3"],
        "sample_rate": sample_rate
    }


@app.get("/api/bandpass")
async def get_bandpass():
    """Generate 3-channel bandpass filtered signal"""
    sample_rate = 1000  # Hz
    duration = 1  # second
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Channel 1: Multiple frequencies, filter around 60Hz
    ch1 = (
        np.sin(2 * np.pi * 10 * t) +
        np.sin(2 * np.pi * 60 * t) +
        np.sin(2 * np.pi * 200 * t) +
        0.2 * np.random.randn(n_samples)
    )

    # Channel 2: Different frequency mix
    ch2 = (
        0.8 * np.sin(2 * np.pi * 15 * t) +
        0.8 * np.sin(2 * np.pi * 65 * t) +
        0.5 * np.sin(2 * np.pi * 180 * t) +
        0.2 * np.random.randn(n_samples)
    )

    # Channel 3: Another frequency mix
    ch3 = (
        0.6 * np.sin(2 * np.pi * 20 * t) +
        0.7 * np.sin(2 * np.pi * 70 * t) +
        0.4 * np.sin(2 * np.pi * 220 * t) +
        0.2 * np.random.randn(n_samples)
    )

    # Bandpass filter around 60Hz (40-80Hz) for each channel
    from scipy import signal as scipy_signal
    sos = scipy_signal.butter(4, [40, 80], 'bandpass', fs=sample_rate, output='sos')
    ch1_filtered = scipy_signal.sosfilt(sos, ch1)
    ch2_filtered = scipy_signal.sosfilt(sos, ch2)
    ch3_filtered = scipy_signal.sosfilt(sos, ch3)

    # Downsample
    step = 2

    return {
        "data": {
            "time": t[::step].tolist(),
            "ch1": ch1_filtered[::step].tolist(),
            "ch2": ch2_filtered[::step].tolist(),
            "ch3": ch3_filtered[::step].tolist()
        },
        "labels": ["Bandpass Ch1", "Bandpass Ch2", "Bandpass Ch3"],
        "sample_rate": sample_rate
    }


@app.get("/api/accelerometer")
async def get_accelerometer():
    """Generate 3D accelerometer data (simulated motion)"""
    sample_rate = 100  # Hz
    duration = 10  # seconds
    n_samples = sample_rate * duration

    t = np.linspace(0, duration, n_samples, endpoint=False)

    # Simulate 3D motion with multiple frequency components + noise
    # X-axis: figure-8 pattern
    x = np.sin(2 * np.pi * 0.5 * t) + 0.1 * np.random.randn(n_samples)

    # Y-axis: circular motion with drift
    y = np.cos(2 * np.pi * 0.5 * t) + 0.1 * t/duration + 0.1 * np.random.randn(n_samples)

    # Z-axis: oscillating up/down with some acceleration events
    z = 0.5 * np.sin(2 * np.pi * 0.3 * t) + 0.2 * np.sin(2 * np.pi * 1.5 * t) + 0.1 * np.random.randn(n_samples)

    return {
        "data": {
            "time": t.tolist(),
            "x": x.tolist(),
            "y": y.tolist(),
            "z": z.tolist()
        },
        "sample_rate": sample_rate,
        "duration": duration
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
