import cv2
import numpy as np
from pathlib import Path
from typing import List, Optional
from transformers import CLIPProcessor, CLIPModel

class ViralMomentDetector:
    """
    Detects viral moments in videos using OpenAI's CLIP model.
    
    Usage:
        detector = ViralMomentDetector()
        timestamps = detector.analyze("data/raw/video.mp4")
    """
    def _init_(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def analyze(
        self,
        video_path: str,
        interval_sec: int = 5,
        concepts: List[str] = ["exciting moment", "funny moment"],
        confidence_threshold: float = 0.7
    ) -> List[float]:
        """
        Analyzes video frames for viral moments.
        
        Args:
            video_path: Path to the video file.
            interval_sec: Analyze every N seconds.
            concepts: Text prompts to match against.
            confidence_threshold: Minimum confidence to flag a moment.
        
        Returns:
            List of timestamps (seconds) where viral moments occur.
        
        Raises:
            FileNotFoundError: If video_path doesn't exist.
        """
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_sec)
        timestamps = []

        try:
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    inputs = self.processor(
                        text=concepts,
                        images=frame_rgb,
                        return_tensors="pt",
                        padding=True
                    )
                    outputs = self.model(**inputs)
                    probs = outputs.logits_per_image.softmax(dim=1)
                    
                    if probs[0][0] > confidence_threshold:
                        timestamps.append(frame_count / fps)
                
                frame_count += 1
        finally:
            cap.release()

        return timestamps

if _name_ == "_main_":
    # Test CLI
    detector = ViralMomentDetector()
    print(detector.analyze("data/raw/test_video.mp4"))