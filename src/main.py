import argparse
from typing import List, Optional
from pathlib import Path
from downloader.youtube_dl import download_video
from ai.clip_analyzer import ViralMomentDetector
from utils.video_utils import extract_clip
from utils.logger import setup_logger

logger = setup_logger()

def process_video(
    url: str,
    output_dir: str = "data/processed",
    clip_duration: float = 15.0
) -> List[str]:
    """
    Full pipeline: Download → Analyze → Extract.
    
    Args:
        url: YouTube URL.
        output_dir: Where to save clips.
        clip_duration: Length of clips in seconds.
    
    Returns:
        List of paths to extracted clips.
    """
    try:
        # 1. Download
        logger.info(f"Downloading: {url}")
        video_path = download_video(url)
        
        # 2. Detect viral moments
        logger.info("Analyzing for viral moments...")
        detector = ViralMomentDetector()
        timestamps = detector.analyze(video_path)
        
        # 3. Extract clips
        clip_paths = []
        for ts in timestamps:
            clip_path = extract_clip(
                video_path,
                start_time=ts,
                duration=clip_duration,
                output_dir=output_dir
            )
            clip_paths.append(clip_path)
            logger.info(f"Extracted clip: {clip_path}")
        
        return clip_paths

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if _name_ == "_main_":
    parser = argparse.ArgumentParser(
        description="Extract viral clips from YouTube videos."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="YouTube video URL"
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Output directory for clips"
    )
    args = parser.parse_args()
    
    process_video(args.url, args.output_dir)