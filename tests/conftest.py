"""Pytest configuration and fixtures"""
import pytest
import numpy as np


@pytest.fixture
def sample_accelerometer_data():
    """Generate sample accelerometer data for testing"""
    return {
        'time': np.arange(0, 10, 0.01),
        'x': np.sin(np.arange(0, 10, 0.01) * 0.1),
        'y': np.cos(np.arange(0, 10, 0.01) * 0.1),
        'z': np.sin(np.arange(0, 10, 0.01) * 0.05)
    }


@pytest.fixture
def sample_signal_data():
    """Generate sample signal data for testing"""
    return {
        'time': np.arange(0, 2, 0.001),
        'ch1': np.sin(np.arange(0, 2, 0.001) * 0.2),
        'ch2': np.sin(np.arange(0, 2, 0.001) * 0.3),
        'ch3': np.sin(np.arange(0, 2, 0.001) * 0.4)
    }


@pytest.fixture
def windowing_simulator():
    """Create a windowing simulator instance"""
    from tests.test_windowing import WindowingSimulator
    return WindowingSimulator()
