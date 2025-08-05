import pytest
from pathlib import Path

@pytest.fixture
def temp_video_file(tmp_path):
    """Creates a dummy video file for testing."""
    video_path = tmp_path / "test_video.mp4"
    video_path.touch()  # Create empty file
    return str(video_path)