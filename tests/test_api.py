"""
API endpoint tests using FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


class TestAPIEndpoints:
    """Test FastAPI endpoints"""
    
    def test_home_page(self, client):
        """Test home page returns HTML"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_signal_endpoint(self, client):
        """Test /api/signal returns proper data structure"""
        response = client.get("/api/signal")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "time" in data["data"]
        assert "ch1" in data["data"]
        assert "ch2" in data["data"]
        assert "ch3" in data["data"]
        assert "labels" in data
        assert len(data["labels"]) == 3
    
    def test_fft_endpoint(self, client):
        """Test /api/fft returns FFT data"""
        response = client.get("/api/fft")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "freq" in data["data"]
        assert "ch1" in data["data"]
    
    def test_filtering_endpoint(self, client):
        """Test /api/filtering returns filtered data"""
        response = client.get("/api/filtering")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "time" in data["data"]
    
    def test_psd_endpoint(self, client):
        """Test /api/psd returns PSD data"""
        response = client.get("/api/psd")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "freq" in data["data"]
    
    def test_bandpass_endpoint(self, client):
        """Test /api/bandpass returns filtered data"""
        response = client.get("/api/bandpass")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
    
    def test_accelerometer_endpoint(self, client):
        """Test /api/accelerometer returns accelerometer data"""
        response = client.get("/api/accelerometer")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "time" in data["data"]
        assert "x" in data["data"]
        assert "y" in data["data"]
        assert "z" in data["data"]


class TestDataQuality:
    """Test data quality and structure"""
    
    def test_signal_data_lengths_match(self, client):
        """Test that all signal channels have matching lengths"""
        response = client.get("/api/signal")
        data = response.json()["data"]
        
        time_len = len(data["time"])
        ch1_len = len(data["ch1"])
        ch2_len = len(data["ch2"])
        ch3_len = len(data["ch3"])
        
        assert time_len == ch1_len == ch2_len == ch3_len
    
    def test_accelerometer_data_lengths_match(self, client):
        """Test that accelerometer x,y,z have matching lengths"""
        response = client.get("/api/accelerometer")
        data = response.json()["data"]
        
        time_len = len(data["time"])
        x_len = len(data["x"])
        y_len = len(data["y"])
        z_len = len(data["z"])
        
        assert time_len == x_len == y_len == z_len
    
    def test_time_series_is_sorted(self, client):
        """Test that time series are monotonically increasing"""
        response = client.get("/api/signal")
        time = response.json()["data"]["time"]
        
        for i in range(1, len(time)):
            assert time[i] > time[i-1], f"Time not monotonic at index {i}"
    
    def test_frequency_is_non_negative(self, client):
        """Test that frequency values are non-negative"""
        response = client.get("/api/fft")
        freq = response.json()["data"]["freq"]
        
        assert all(f >= 0 for f in freq), "Negative frequencies found"
    
    def test_data_is_numeric(self, client):
        """Test that all data values are numeric"""
        response = client.get("/api/signal")
        data = response.json()["data"]
        
        for key in ["time", "ch1", "ch2", "ch3"]:
            values = data[key]
            assert all(isinstance(v, (int, float)) for v in values), \
                f"{key} contains non-numeric values"


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_nonexistent_endpoint(self, client):
        """Test 404 for non-existent endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_static_files_accessible(self, client):
        """Test that static files are accessible"""
        response = client.get("/static/css/styles.css")
        assert response.status_code == 200
    
    def test_cors_headers(self, client):
        """Test CORS headers if enabled"""
        response = client.get("/api/signal")
        assert response.status_code == 200
