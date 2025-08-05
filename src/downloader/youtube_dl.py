import yt_dlp
from pathlib import Path

def download_video(url: str, output_dir: str = "data/raw") -> str:
    """
    Downloads a YouTube video and returns its absolute path.
    
    Args:
        url: YouTube video URL.
        output_dir: Directory to save the video (default: "data/raw").
    
    Returns:
        str: Path to the downloaded video (e.g., "data/raw/video_title.mp4").
    
    Raises:
        yt_dlp.DownloadError: If download fails.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)  # Ensure dir exists
    
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "quiet": True,  # Suppress verbose logs
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            return f"{output_dir}/{info['title']}.mp4"
    except Exception as e:
        raise yt_dlp.DownloadError(f"Failed to download {url}: {str(e)}")

if _name_ == "_main_":
    # Test the function
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="YouTube URL")
    args = parser.parse_args()
    
    try:
        path = download_video(args.url)
        print(f"Success! Video saved to: {path}")
    except Exception as e:
        print(f"Error: {str(e)}")