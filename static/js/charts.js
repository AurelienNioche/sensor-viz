let charts = {};
let accelerometerData = null;
let currentWindowSize = 0.5;  // Start with 0.5 seconds for better windowing
let chartData = {};
let activeChart = 'accelerometer';
let clickedTime = null;

// Update 3D trajectory based on active chart
function update3DTrajectory(chartName, chartTitle, centerTime = null) {
    console.log(`update3DTrajectory called: chart=${chartName}, centerTime=${centerTime}, currentClickedTime=${clickedTime}`);
    
    activeChart = chartName;
    
    if (centerTime !== null) {
        clickedTime = centerTime;
    }
    
    console.log(`  After update: activeChart=${activeChart}, clickedTime=${clickedTime}, windowSize=${currentWindowSize}`);

    // Update active state styling
    document.querySelectorAll('.chart-section').forEach(section => {
        section.classList.remove('active');
    });

    const chartElement = document.getElementById(`chart-${chartName}`);
    if (chartElement && chartElement.parentElement) {
        chartElement.parentElement.classList.add('active');
    }

    // Update description
    const descElem = document.getElementById('trajectory-description');

    if (chartName === 'accelerometer') {
        if (clickedTime === null) {
            descElem.textContent = 'Default: Accelerometer data showing first N seconds (click any time series above to visualize it in 3D)';
        } else {
            descElem.textContent = `Accelerometer data centered at t=${clickedTime.toFixed(2)}s (use slider to adjust window)`;
        }
        renderAccelerometerPlot();
        return;
    }

    // Use 3 channels directly as X, Y, Z
    const storedData = chartData[chartName];
    if (!storedData || !storedData.data) {
        console.error('No data for chart:', chartName);
        return;
    }

    const { ch1, ch2, ch3 } = storedData.data;
    const timeAxis = storedData.data.time || storedData.data.freq || [];

    console.log(`  Data range: ${timeAxis[0]} to ${timeAxis[timeAxis.length-1]}, total: ${timeAxis.length} points`);

    // Apply windowing if a time was clicked
    let windowedCh1, windowedCh2, windowedCh3, windowedTime;
    let windowStart, windowEnd;

    if (clickedTime !== null && timeAxis.length > 0) {
        // Window centered on clicked time
        const halfWindow = currentWindowSize / 2;
        windowStart = Math.max(0, clickedTime - halfWindow);
        windowEnd = clickedTime + halfWindow;
        
        console.log(`  Windowing ${chartName}: center=${clickedTime}, halfWindow=${halfWindow}, window=${windowStart} to ${windowEnd}`);

        const startIdx = timeAxis.findIndex(t => t >= windowStart);
        const endIdx = timeAxis.findIndex(t => t > windowEnd);
        const actualStartIdx = startIdx === -1 ? 0 : startIdx;
        const actualEndIdx = endIdx === -1 ? timeAxis.length : endIdx;

        console.log(`  Found indices: start=${actualStartIdx}, end=${actualEndIdx}`);

        windowedCh1 = ch1.slice(actualStartIdx, actualEndIdx);
        windowedCh2 = ch2.slice(actualStartIdx, actualEndIdx);
        windowedCh3 = ch3.slice(actualStartIdx, actualEndIdx);
        windowedTime = timeAxis.slice(actualStartIdx, actualEndIdx);
        
        console.log(`  Result: ${windowedTime.length} points, actual range: ${windowedTime[0]?.toFixed(3)} to ${windowedTime[windowedTime.length-1]?.toFixed(3)}`);

        const axis = chartName === 'fft' || chartName === 'psd' ? 'frequency' : 'time';
        const unit = chartName === 'fft' || chartName === 'psd' ? 'Hz' : 's';
        descElem.textContent = `3D Trajectory: ${chartTitle} - windowed around ${axis}=${clickedTime.toFixed(2)}${unit} (±${(currentWindowSize/2).toFixed(1)}${unit})`;
    } else {
        // Use all data
        windowedCh1 = ch1;
        windowedCh2 = ch2;
        windowedCh3 = ch3;
        windowedTime = timeAxis;
        console.log(`  Using full dataset: ${windowedTime.length} points`);
        descElem.textContent = `3D Trajectory: ${chartTitle} - full dataset (Ch1=X, Ch2=Y, Ch3=Z)`;
    }

    // Create color gradient
    const colors = windowedCh1.map((_, i) => {
        const ratio = i / windowedCh1.length;
        return `rgb(${Math.round(ratio * 255)}, ${Math.round((1 - ratio) * 100)}, ${Math.round((1 - ratio) * 255)})`;
    });

    const trace = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: windowedCh1,
        y: windowedCh2,
        z: windowedCh3,
        line: {
            color: colors,
            width: 4
        },
        marker: {
            size: 3,
            color: colors,
        },
        text: windowedTime.map((v, i) => `t=${v.toFixed(3)}s`),
        hoverinfo: 'text+x+y+z'
    };

    const layout = {
        title: `3D Trajectory - ${chartTitle}`,
        scene: {
            xaxis: { title: 'Channel 1' },
            yaxis: { title: 'Channel 2' },
            zaxis: { title: 'Channel 3' },
            camera: {
                eye: { x: 1.5, y: 1.5, z: 1.3 }
            }
        },
        margin: { l: 0, r: 0, b: 0, t: 40 },
        height: 450
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };

    Plotly.newPlot('chart-accelerometer', [trace], layout, config);
}

function renderAccelerometerPlot() {
    if (!accelerometerData) return;

    const { time, x, y, z } = accelerometerData;

    let minTime, maxTime, startIdx, actualEndIdx;

    if (clickedTime !== null) {
        // Window centered on clicked time
        const halfWindow = currentWindowSize / 2;
        minTime = Math.max(0, clickedTime - halfWindow);
        maxTime = clickedTime + halfWindow;
        
        console.log(`renderAccelerometerPlot: CENTERED mode - clickedTime=${clickedTime}, window=${minTime} to ${maxTime}`);

        const foundStartIdx = time.findIndex(t => t >= minTime);
        const foundEndIdx = time.findIndex(t => t > maxTime);
        startIdx = foundStartIdx === -1 ? 0 : foundStartIdx;
        actualEndIdx = foundEndIdx === -1 ? time.length : foundEndIdx;
    } else {
        // Default: first N seconds from t=0
        minTime = 0;
        maxTime = currentWindowSize;
        
        console.log(`renderAccelerometerPlot: DEFAULT mode - t=0 to ${maxTime}`);

        startIdx = 0;
        const endIdx = time.findIndex(t => t > maxTime);
        actualEndIdx = endIdx === -1 ? time.length : endIdx;
    }

    const windowTime = time.slice(startIdx, actualEndIdx);
    const windowX = x.slice(startIdx, actualEndIdx);
    const windowY = y.slice(startIdx, actualEndIdx);
    const windowZ = z.slice(startIdx, actualEndIdx);
    
    console.log(`  Result: ${windowTime.length} points, range ${windowTime[0]?.toFixed(3)} to ${windowTime[windowTime.length-1]?.toFixed(3)}`);

    // Create color gradient based on time (older = blue, newer = red)
    const colors = windowTime.map((t, i) => {
        const ratio = i / windowTime.length;
        return `rgb(${Math.round(ratio * 255)}, ${Math.round((1 - ratio) * 100)}, ${Math.round((1 - ratio) * 255)})`;
    });

    const trace = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: windowX,
        y: windowY,
        z: windowZ,
        line: {
            color: colors,
            width: 4
        },
        marker: {
            size: 3,
            color: colors,
        },
        text: windowTime.map(t => `Time: ${t.toFixed(2)}s`),
        hoverinfo: 'text+x+y+z'
    };

    const titleText = clickedTime !== null 
        ? `3D Accelerometer Trajectory (t=${minTime.toFixed(2)} to t=${maxTime.toFixed(2)}s, ${windowTime.length} points)`
        : `3D Accelerometer Trajectory (t=0 to t=${currentWindowSize}s, ${windowTime.length} points)`;

    const layout = {
        title: titleText,
        scene: {
            xaxis: { title: 'X Acceleration (g)' },
            yaxis: { title: 'Y Acceleration (g)' },
            zaxis: { title: 'Z Acceleration (g)' },
            camera: {
                eye: { x: 1.5, y: 1.5, z: 1.3 }
            }
        },
        margin: { l: 0, r: 0, b: 0, t: 40 },
        height: 450
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };

    Plotly.newPlot('chart-accelerometer', [trace], layout, config);
}

function initSignalChart() {
    fetch('/api/signal')
        .then(response => response.json())
        .then(result => {
            chartData.signal = result;

            const opts = {
                title: "Time Domain - 3-Channel Signal",
                width: document.getElementById('chart-signal').offsetWidth,
                height: 250,
                series: [
                    {},
                    {
                        label: result.labels[0],
                        stroke: "#667eea",
                        width: 1.5,
                    },
                    {
                        label: result.labels[1],
                        stroke: "#f59e0b",
                        width: 1.5,
                    },
                    {
                        label: result.labels[2],
                        stroke: "#10b981",
                        width: 1.5,
                    }
                ],
                axes: [
                    {
                        label: "Time (s)",
                        values: (u, vals) => vals.map(v => v.toFixed(3))
                    },
                    {
                        side: 1,
                        label: "Amplitude",
                    }
                ],
                scales: {
                    x: {
                        time: false,
                    }
                }
            };

            // Convert data format for uPlot
            const plotData = [
                result.data.time,
                result.data.ch1,
                result.data.ch2,
                result.data.ch3
            ];

            charts.signal = new uPlot(opts, plotData, document.getElementById('chart-signal'));

            // Add canvas click handler to detect time
            const section = document.getElementById('chart-signal').parentElement;
            section.classList.add('clickable');
            charts.signal.root.querySelector('.u-over').addEventListener('click', (e) => {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const timeAtClick = charts.signal.posToVal(x, 'x');
                update3DTrajectory('signal', '3-Channel Signal', timeAtClick);
            });
        });
}

function initFFTChart() {
    fetch('/api/fft')
        .then(response => response.json())
        .then(result => {
            chartData.fft = result;

            const opts = {
                title: "Frequency Domain - 3-Channel FFT",
                width: document.getElementById('chart-fft').offsetWidth,
                height: 250,
                series: [
                    {},
                    {
                        label: result.labels[0],
                        stroke: "#667eea",
                        width: 1.5,
                    },
                    {
                        label: result.labels[1],
                        stroke: "#f59e0b",
                        width: 1.5,
                    },
                    {
                        label: result.labels[2],
                        stroke: "#10b981",
                        width: 1.5,
                    }
                ],
                axes: [
                    {
                        label: "Frequency (Hz)",
                        values: (u, vals) => vals.map(v => v.toFixed(0))
                    },
                    {
                        side: 1,
                        label: "Magnitude",
                    }
                ],
                scales: {
                    x: {
                        time: false,
                    }
                }
            };

            const plotData = [
                result.data.freq,
                result.data.ch1,
                result.data.ch2,
                result.data.ch3
            ];

            charts.fft = new uPlot(opts, plotData, document.getElementById('chart-fft'));

            // Add canvas click handler
            const section = document.getElementById('chart-fft').parentElement;
            section.classList.add('clickable');
            charts.fft.root.querySelector('.u-over').addEventListener('click', (e) => {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const freqAtClick = charts.fft.posToVal(x, 'x');
                update3DTrajectory('fft', 'FFT Spectrum', freqAtClick);
            });
        });
}

function initFilteringChart() {
    fetch('/api/filtering')
        .then(response => response.json())
        .then(result => {
            chartData.filtering = result;

            const opts = {
                title: "Signal Filtering - 3-Channel Low-pass",
                width: document.getElementById('chart-filtering').offsetWidth,
                height: 250,
                series: [
                    {},
                    {
                        label: result.labels[0],
                        stroke: "#667eea",
                        width: 1.5,
                    },
                    {
                        label: result.labels[1],
                        stroke: "#f59e0b",
                        width: 1.5,
                    },
                    {
                        label: result.labels[2],
                        stroke: "#10b981",
                        width: 1.5,
                    }
                ],
                axes: [
                    {
                        label: "Time (s)",
                        values: (u, vals) => vals.map(v => v.toFixed(3))
                    },
                    {
                        side: 1,
                        label: "Amplitude",
                    }
                ],
                scales: {
                    x: {
                        time: false,
                    }
                }
            };

            const plotData = [
                result.data.time,
                result.data.ch1,
                result.data.ch2,
                result.data.ch3
            ];

            charts.filtering = new uPlot(opts, plotData, document.getElementById('chart-filtering'));

            // Add canvas click handler
            const section = document.getElementById('chart-filtering').parentElement;
            section.classList.add('clickable');
            charts.filtering.root.querySelector('.u-over').addEventListener('click', (e) => {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const timeAtClick = charts.filtering.posToVal(x, 'x');
                update3DTrajectory('filtering', 'Filtered Signal', timeAtClick);
            });
        });
}

function initPSDChart() {
    fetch('/api/psd')
        .then(response => response.json())
        .then(result => {
            chartData.psd = result;

            const opts = {
                title: "Power Spectral Density - 3-Channel",
                width: document.getElementById('chart-psd').offsetWidth,
                height: 250,
                series: [
                    {},
                    {
                        label: result.labels[0],
                        stroke: "#667eea",
                        width: 1.5,
                    },
                    {
                        label: result.labels[1],
                        stroke: "#f59e0b",
                        width: 1.5,
                    },
                    {
                        label: result.labels[2],
                        stroke: "#10b981",
                        width: 1.5,
                    }
                ],
                axes: [
                    {
                        label: "Frequency (Hz)",
                        values: (u, vals) => vals.map(v => v.toFixed(0))
                    },
                    {
                        side: 1,
                        label: "Power/Frequency",
                    }
                ],
                scales: {
                    x: {
                        time: false,
                    }
                }
            };

            const plotData = [
                result.data.freq,
                result.data.ch1,
                result.data.ch2,
                result.data.ch3
            ];

            charts.psd = new uPlot(opts, plotData, document.getElementById('chart-psd'));

            // Add canvas click handler
            const section = document.getElementById('chart-psd').parentElement;
            section.classList.add('clickable');
            charts.psd.root.querySelector('.u-over').addEventListener('click', (e) => {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const freqAtClick = charts.psd.posToVal(x, 'x');
                update3DTrajectory('psd', 'Power Spectral Density', freqAtClick);
            });
        });
}

function initBandpassChart() {
    fetch('/api/bandpass')
        .then(response => response.json())
        .then(result => {
            chartData.bandpass = result;

            const opts = {
                title: "Bandpass Filtering - 3-Channel",
                width: document.getElementById('chart-bandpass').offsetWidth,
                height: 250,
                series: [
                    {},
                    {
                        label: result.labels[0],
                        stroke: "#667eea",
                        width: 1.5,
                    },
                    {
                        label: result.labels[1],
                        stroke: "#f59e0b",
                        width: 1.5,
                    },
                    {
                        label: result.labels[2],
                        stroke: "#10b981",
                        width: 1.5,
                    }
                ],
                axes: [
                    {
                        label: "Time (s)",
                        values: (u, vals) => vals.map(v => v.toFixed(3))
                    },
                    {
                        side: 1,
                        label: "Amplitude",
                    }
                ],
                scales: {
                    x: {
                        time: false,
                    }
                }
            };

            const plotData = [
                result.data.time,
                result.data.ch1,
                result.data.ch2,
                result.data.ch3
            ];

            charts.bandpass = new uPlot(opts, plotData, document.getElementById('chart-bandpass'));

            // Add canvas click handler
            const section = document.getElementById('chart-bandpass').parentElement;
            section.classList.add('clickable');
            charts.bandpass.root.querySelector('.u-over').addEventListener('click', (e) => {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const timeAtClick = charts.bandpass.posToVal(x, 'x');
                console.log(`CLICK on bandpass: timeAtClick=${timeAtClick}, data range: ${result.data.time[0]} to ${result.data.time[result.data.time.length-1]}`);
                update3DTrajectory('bandpass', 'Bandpass Filtered Signal', timeAtClick);
            });
        });
}

function initAccelerometerChart() {
    fetch('/api/accelerometer')
        .then(response => response.json())
        .then(result => {
            accelerometerData = result.data;
            renderAccelerometerPlot();

            // Setup slider event listener
            const slider = document.getElementById('window-slider');
            const valueDisplay = document.getElementById('window-value');

            // Initialize display
            valueDisplay.textContent = currentWindowSize.toFixed(1);
            
            slider.addEventListener('input', (e) => {
                currentWindowSize = parseFloat(e.target.value);
                valueDisplay.textContent = currentWindowSize.toFixed(1);
                
                console.log(`Slider adjusted to ${currentWindowSize}, activeChart=${activeChart}, clickedTime=${clickedTime}`);

                // Re-render the currently active chart with new window size
                const chartTitles = {
                    'accelerometer': 'Accelerometer',
                    'signal': '3-Channel Signal',
                    'fft': 'FFT Spectrum',
                    'filtering': 'Filtered Signal',
                    'psd': 'Power Spectral Density',
                    'bandpass': 'Bandpass Filtered Signal'
                };
                
                // Don't pass clickedTime as parameter, it's already set globally
                // Just trigger the update which will use the existing clickedTime value
                if (activeChart === 'accelerometer') {
                    renderAccelerometerPlot();
                } else {
                    update3DTrajectory(activeChart, chartTitles[activeChart]);
                }
            });

            // Reset button to go back to default accelerometer view
            const resetBtn = document.getElementById('reset-view');
            resetBtn.addEventListener('click', () => {
                console.log('Reset button clicked');
                clickedTime = null;
                activeChart = 'accelerometer';
                currentWindowSize = parseFloat(slider.value); // Keep current slider value
                update3DTrajectory('accelerometer', 'Accelerometer', null);
            });
        });
}

window.addEventListener('resize', () => {
    Object.values(charts).forEach(chart => {
        if (chart && chart.root && chart.root.parentElement) {
            chart.setSize({
                width: chart.root.parentElement.offsetWidth,
                height: 250
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    initSignalChart();
    initFFTChart();
    initFilteringChart();
    initPSDChart();
    initBandpassChart();
    initAccelerometerChart();
});
