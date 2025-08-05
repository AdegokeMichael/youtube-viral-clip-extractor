import subprocess
from pathlib import Path
from typing import Optional

def extract_clip(
    video_path: str,
    start_time: float,
    duration: float = 15.0,
    output_dir: str = "data/processed",
    output_filename: Optional[str] = None
) -> str:
    """
    Extracts a clip from a video using FFmpeg.
    
    Args:
        video_path: Input video file.
        start_time: Start time in seconds.
        duration: Clip duration in seconds.
        output_dir: Directory to save clips.
        output_filename: Custom filename (default: clip_{start_time}.mp4).
    
    Returns:
        Path to the extracted clip.
    
    Raises:
        FileNotFoundError: If video_path doesn't exist.
        subprocess.CalledProcessError: If FFmpeg fails.
    """
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = f"{output_dir}/{output_filename or f'clip_{start_time}.mp4'}"

    try:
        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-ss", str(start_time),
            "-t", str(duration),
            "-c:v", "copy",  # No re-encoding (fast)
            "-c:a", "copy",
            "-loglevel", "error",  # Suppress FFmpeg noise
            output_path
        ], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e.stderr}")

if _name_ == "_main_":
    # Test CLI
    print(extract_clip("data/raw/test_video.mp4", start_time=10.0))