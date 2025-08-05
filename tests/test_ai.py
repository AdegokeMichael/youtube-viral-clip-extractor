import pytest
import cv2
import numpy as np
from unittest.mock import MagicMock
from ai.clip_analyzer import ViralMomentDetector

def test_analyze_viral_moments(mocker):
    """Test frame analysis with mocked CLIP model."""
    # Mock dependencies
    mock_processor = MagicMock()
    mock_model = MagicMock()
    mocker.patch(
        "ai.clip_analyzer.CLIPModel.from_pretrained",
        return_value=mock_model
    )
    mocker.patch(
        "ai.clip_analyzer.CLIPProcessor.from_pretrained",
        return_value=mock_processor
    )

    # Mock video capture
    mock_cap = mocker.patch("cv2.VideoCapture")
    mock_cap.return_value.isOpened.return_value = True
    mock_cap.return_value.read.side_effect = [
        (True, np.zeros((480, 640, 3), dtype=np.uint8)),  # Fake frame
        (False, None)  # End of video
    ]
    mock_cap.return_value.get.return_value = 30  # FPS

    # Mock CLIP output (simulate "exciting moment" detection)
    mock_model.return_value.logits_per_image.softmax.return_value = [[0.8, 0.2]]  # 80% confidence

    # Run test
    detector = ViralMomentDetector()
    timestamps = detector.analyze("fake_video.mp4", interval_sec=1)

    # Assertions
    assert len(timestamps) == 1  # Found 1 viral moment
    mock_cap.return_value.release.assert_called_once()

def test_analyze_missing_file():
    """Test error for missing video file."""
    detector = ViralMomentDetector()
    with pytest.raises(FileNotFoundError):
        detector.analyze("nonexistent.mp4")