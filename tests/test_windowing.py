"""
Test suite for windowing behavior

This tests the core windowing logic that's implemented in JavaScript.
The Python implementation mirrors the JS behavior for testing purposes.
"""
import pytest
import numpy as np
from typing import Optional, Dict, Any


class WindowingSimulator:
    """Simulates the windowing logic from charts.js"""
    
    def __init__(self):
        self.current_window_size = 2.0
        self.active_chart = 'accelerometer'
        self.clicked_time: Optional[float] = None
        
        self.accelerometer_data = {
            'time': np.arange(0, 10, 0.01),
            'x': np.sin(np.arange(0, 10, 0.01) * 0.1),
            'y': np.cos(np.arange(0, 10, 0.01) * 0.1),
            'z': np.sin(np.arange(0, 10, 0.01) * 0.05)
        }
        
        self.signal_data = {
            'time': np.arange(0, 2, 0.001),
            'ch1': np.sin(np.arange(0, 2, 0.001) * 0.2),
            'ch2': np.sin(np.arange(0, 2, 0.001) * 0.3),
            'ch3': np.sin(np.arange(0, 2, 0.001) * 0.4)
        }
    
    def get_windowed_data(self, chart_name: Optional[str] = None) -> Dict[str, Any]:
        """Get windowed data for the specified chart"""
        chart_name = chart_name or self.active_chart
        
        if chart_name == 'accelerometer':
            return self.get_accelerometer_window()
        elif chart_name == 'signal':
            return self.get_signal_window()
        
        return {}
    
    def get_accelerometer_window(self) -> Dict[str, Any]:
        """Get windowed accelerometer data"""
        time = self.accelerometer_data['time']
        x = self.accelerometer_data['x']
        y = self.accelerometer_data['y']
        z = self.accelerometer_data['z']
        
        if self.clicked_time is not None:
            half_window = self.current_window_size / 2
            min_time = max(0, self.clicked_time - half_window)
            max_time = self.clicked_time + half_window
            
            start_idx = np.searchsorted(time, min_time, side='left')
            end_idx = np.searchsorted(time, max_time, side='right')
        else:
            min_time = 0
            max_time = self.current_window_size
            
            start_idx = 0
            end_idx = np.searchsorted(time, max_time, side='right')
        
        window_time = time[start_idx:end_idx]
        
        return {
            'time': window_time,
            'x': x[start_idx:end_idx],
            'y': y[start_idx:end_idx],
            'z': z[start_idx:end_idx],
            'min_time': min_time,
            'max_time': max_time,
            'num_points': len(window_time)
        }
    
    def get_signal_window(self) -> Dict[str, Any]:
        """Get windowed signal data"""
        time = self.signal_data['time']
        ch1 = self.signal_data['ch1']
        ch2 = self.signal_data['ch2']
        ch3 = self.signal_data['ch3']
        
        if self.clicked_time is not None:
            half_window = self.current_window_size / 2
            min_time = max(0, self.clicked_time - half_window)
            max_time = self.clicked_time + half_window
            
            start_idx = np.searchsorted(time, min_time, side='left')
            end_idx = np.searchsorted(time, max_time, side='right')
        else:
            min_time = time[0]
            max_time = time[-1]
            start_idx = 0
            end_idx = len(time)
        
        window_time = time[start_idx:end_idx]
        
        return {
            'time': window_time,
            'ch1': ch1[start_idx:end_idx],
            'ch2': ch2[start_idx:end_idx],
            'ch3': ch3[start_idx:end_idx],
            'min_time': min_time,
            'max_time': max_time,
            'num_points': len(window_time)
        }
    
    def click_on_chart(self, chart_name: str, click_time: float) -> Dict[str, Any]:
        """Simulate clicking on a chart at a specific time"""
        self.active_chart = chart_name
        self.clicked_time = click_time
        return self.get_windowed_data(chart_name)
    
    def adjust_slider(self, new_window_size: float) -> Dict[str, Any]:
        """Simulate adjusting the window size slider"""
        self.current_window_size = new_window_size
        return self.get_windowed_data(self.active_chart)
    
    def reset(self) -> Dict[str, Any]:
        """Reset to default state"""
        self.active_chart = 'accelerometer'
        self.clicked_time = None
        return self.get_windowed_data('accelerometer')


class TestInitialState:
    """Test initial/default state behavior"""
    
    def test_initial_accelerometer_default(self):
        """Test that accelerometer shows first N seconds from t=0"""
        sim = WindowingSimulator()
        result = sim.get_windowed_data('accelerometer')
        
        assert result['min_time'] == 0
        assert result['max_time'] == 2.0
        assert result['num_points'] > 0
        assert result['time'][0] >= 0
        assert result['time'][-1] <= 2.0
    
    def test_default_window_size(self):
        """Test default window size is 2.0 seconds"""
        sim = WindowingSimulator()
        assert sim.current_window_size == 2.0
    
    def test_no_clicked_time_initially(self):
        """Test that clicked_time is None initially"""
        sim = WindowingSimulator()
        assert sim.clicked_time is None


class TestClickBehavior:
    """Test click-to-center window behavior"""
    
    def test_first_click_centers_window(self):
        """Test clicking centers window on clicked time"""
        sim = WindowingSimulator()
        result = sim.click_on_chart('signal', 1.0)
        
        expected_min = 1.0 - 1.0  # clickTime - windowSize/2
        expected_max = 1.0 + 1.0  # clickTime + windowSize/2
        
        assert abs(result['min_time'] - expected_min) < 0.01
        assert abs(result['max_time'] - expected_max) < 0.01
    
    def test_click_updates_active_chart(self):
        """Test that clicking updates the active chart"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 1.0)
        
        assert sim.active_chart == 'signal'
        assert sim.clicked_time == 1.0
    
    def test_second_click_recenters(self):
        """Test that second click on same chart re-centers window"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 1.5)
        result = sim.click_on_chart('signal', 0.8)
        
        expected_min = max(0, 0.8 - 1.0)
        expected_max = 0.8 + 1.0
        
        assert abs(result['min_time'] - expected_min) < 0.01
        assert abs(result['max_time'] - expected_max) < 0.01
    
    def test_click_different_chart(self):
        """Test clicking different chart switches context"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 1.5)
        result = sim.click_on_chart('accelerometer', 5.0)
        
        assert sim.active_chart == 'accelerometer'
        assert sim.clicked_time == 5.0
        
        expected_min = 5.0 - 1.0
        expected_max = 5.0 + 1.0
        
        assert abs(result['min_time'] - expected_min) < 0.01
        assert abs(result['max_time'] - expected_max) < 0.01
    
    def test_click_at_boundary(self):
        """Test clicking near t=0 boundary"""
        sim = WindowingSimulator()
        result = sim.click_on_chart('signal', 0.5)
        
        assert result['min_time'] >= 0
        assert result['max_time'] > result['min_time']


class TestSliderBehavior:
    """Test slider window size adjustment behavior"""
    
    def test_slider_on_default_view(self):
        """Test slider adjusts window from t=0 when no click"""
        sim = WindowingSimulator()
        result = sim.adjust_slider(3.5)
        
        assert result['min_time'] == 0
        assert abs(result['max_time'] - 3.5) < 0.01
    
    def test_slider_after_click_stays_centered(self):
        """Test slider keeps window centered after click"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 1.0)
        result = sim.adjust_slider(1.0)
        
        expected_min = 1.0 - 0.5
        expected_max = 1.0 + 0.5
        
        assert abs(result['min_time'] - expected_min) < 0.01
        assert abs(result['max_time'] - expected_max) < 0.01
    
    def test_slider_increases_window_size(self):
        """Test increasing slider increases window size"""
        sim = WindowingSimulator()
        initial = sim.get_windowed_data('accelerometer')
        result = sim.adjust_slider(5.0)
        
        assert result['num_points'] > initial['num_points']
        assert result['max_time'] > initial['max_time']
    
    def test_slider_decreases_window_size(self):
        """Test decreasing slider decreases window size"""
        sim = WindowingSimulator()
        sim.adjust_slider(4.0)
        initial = sim.get_windowed_data('accelerometer')
        result = sim.adjust_slider(1.0)
        
        assert result['num_points'] < initial['num_points']
        assert result['max_time'] < initial['max_time']


class TestResetBehavior:
    """Test reset functionality"""
    
    def test_reset_clears_clicked_time(self):
        """Test reset clears the clicked time"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 5.0)
        sim.reset()
        
        assert sim.clicked_time is None
    
    def test_reset_returns_to_accelerometer(self):
        """Test reset returns to accelerometer chart"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 5.0)
        sim.reset()
        
        assert sim.active_chart == 'accelerometer'
    
    def test_reset_preserves_window_size(self):
        """Test reset preserves the current window size"""
        sim = WindowingSimulator()
        sim.adjust_slider(3.5)
        sim.click_on_chart('signal', 1.0)
        result = sim.reset()
        
        assert abs(result['max_time'] - 3.5) < 0.01


class TestComplexScenarios:
    """Test complex multi-step scenarios"""
    
    def test_full_interaction_sequence(self):
        """Test complete interaction: load → click → slider → switch → reset"""
        sim = WindowingSimulator()
        
        initial = sim.get_windowed_data('accelerometer')
        assert initial['min_time'] == 0
        
        click1 = sim.click_on_chart('signal', 1.2)
        assert sim.clicked_time == 1.2
        
        slider1 = sim.adjust_slider(3.0)
        assert sim.current_window_size == 3.0
        assert sim.clicked_time == 1.2
        
        click2 = sim.click_on_chart('accelerometer', 7.0)
        assert sim.clicked_time == 7.0
        assert abs(click2['min_time'] - 5.5) < 0.01
        
        slider2 = sim.adjust_slider(1.5)
        assert abs(slider2['min_time'] - 6.25) < 0.01
        
        reset = sim.reset()
        assert reset['min_time'] == 0
        assert sim.clicked_time is None
    
    def test_rapid_clicks_same_chart(self):
        """Test multiple rapid clicks on same chart"""
        sim = WindowingSimulator()
        
        for t in [0.5, 1.0, 1.5, 1.2, 0.8]:
            result = sim.click_on_chart('signal', t)
            assert abs(sim.clicked_time - t) < 0.001
    
    def test_slider_adjustments_preserve_state(self):
        """Test that slider adjustments don't corrupt state"""
        sim = WindowingSimulator()
        sim.click_on_chart('signal', 1.0)
        
        for size in [1.0, 2.0, 3.0, 1.5, 2.5]:
            result = sim.adjust_slider(size)
            assert sim.clicked_time == 1.0
            assert sim.current_window_size == size


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_click_at_zero(self):
        """Test clicking at t=0"""
        sim = WindowingSimulator()
        result = sim.click_on_chart('signal', 0.0)
        
        assert result['min_time'] == 0
        assert result['max_time'] > 0
    
    def test_click_beyond_data_range(self):
        """Test clicking beyond available data range"""
        sim = WindowingSimulator()
        result = sim.click_on_chart('signal', 10.0)
        
        assert result['min_time'] >= 0
        assert result['num_points'] >= 0
    
    def test_very_small_window(self):
        """Test very small window size"""
        sim = WindowingSimulator()
        result = sim.adjust_slider(0.1)
        
        assert result['num_points'] > 0
        assert result['max_time'] > result['min_time']
    
    def test_very_large_window(self):
        """Test very large window size"""
        sim = WindowingSimulator()
        result = sim.adjust_slider(50.0)
        
        assert result['num_points'] > 0
    
    def test_window_size_zero(self):
        """Test that window size zero is handled"""
        sim = WindowingSimulator()
        sim.current_window_size = 0.0
        result = sim.get_windowed_data('accelerometer')
        
        assert result['min_time'] == result['max_time']


@pytest.mark.parametrize("chart,click_time,expected_active", [
    ('signal', 1.0, 'signal'),
    ('accelerometer', 5.0, 'accelerometer'),
    ('signal', 0.5, 'signal'),
    ('accelerometer', 8.0, 'accelerometer'),
])
def test_click_sets_correct_chart(chart, click_time, expected_active):
    """Parametrized test for chart switching"""
    sim = WindowingSimulator()
    sim.click_on_chart(chart, click_time)
    assert sim.active_chart == expected_active


@pytest.mark.parametrize("window_size", [0.5, 1.0, 2.0, 3.0, 5.0, 10.0])
def test_various_window_sizes(window_size):
    """Parametrized test for different window sizes"""
    sim = WindowingSimulator()
    result = sim.adjust_slider(window_size)
    assert abs(result['max_time'] - window_size) < 0.01
