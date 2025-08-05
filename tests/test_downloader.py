import pytest
from unittest.mock import patch
from downloader.youtube_dl import download_video
from pathlib import Path

def test_download_video_success(mocker):
    """Test successful video download."""
    # Mock yt_dlp to avoid real network calls
    mock_ydl = mocker.patch("downloader.youtube_dl.yt_dlp.YoutubeDL")
    mock_ydl.return_value._enter_.return_value.extract_info.return_value = {
        "title": "test_video"
    }

    # Call function
    output_path = download_video("https://youtube.com/watch?v=123", "data/test_raw")

    # Assertions
    assert output_path == "data/test_raw/test_video.mp4"
    mock_ydl.return_value._enter_.return_value.download.assert_called_once()

def test_download_video_missing_dir():
    """Test automatic directory creation."""
    test_dir = "data/temp_dir"
    Path(test_dir).mkdir(exist_ok=True)  # Ensure clean start
    
    with patch("downloader.youtube_dl.yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value._enter_.return_value.extract_info.return_value = {
            "title": "test_video"
        }
        download_video("https://youtube.com/watch?v=123", test_dir)
    
    assert Path(test_dir).exists()  # Dir was created
    Path(test_dir).rmdir()  # Cleanup

def test_download_video_failure(mocker):
    """Test download error handling."""
    mocker.patch(
        "downloader.youtube_dl.yt_dlp.YoutubeDL",
        side_effect=Exception("Download failed")
    )
    
    with pytest.raises(Exception, match="Download failed"):
        download_video("invalid_url")