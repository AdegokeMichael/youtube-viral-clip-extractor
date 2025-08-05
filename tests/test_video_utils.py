import pytest
from unittest.mock import patch
from utils.video_utils import extract_clip
import subprocess

def test_extract_clip_success(mocker):
    """Test successful clip extraction."""
    # Mock FFmpeg
    mocker.patch("subprocess.run", return_value=MagicMock(returncode=0))

    # Call function
    output_path = extract_clip(
        "data/raw/test.mp4",
        start_time=10.0,
        output_dir="data/test_processed"
    )

    # Assertions
    assert output_path == "data/test_processed/clip_10.0.mp4"
    subprocess.run.assert_called_once()

def test_extract_clip_missing_video():
    """Test error for missing input video."""
    with pytest.raises(FileNotFoundError):
        extract_clip("nonexistent.mp4", start_time=0)

def test_extract_clip_ffmpeg_failure(mocker):
    """Test FFmpeg failure handling."""
    mocker.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "ffmpeg", "Error")
    )
    
    with pytest.raises(RuntimeError, match="FFmpeg failed"):
        extract_clip("data/raw/test.mp4", start_time=0)