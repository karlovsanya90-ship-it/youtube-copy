import logging
import subprocess
import os
from pathlib import Path
from app.workers.celery_app import celery_app
from app.core.config import settings

log = logging.getLogger(__name__)

def run_ffmpeg_hls(input_path: Path, output_dir: Path, width: int, height: int, bitrate: str):
    """Запускает ffmpeg для создания HLS-плейлиста."""
    output_dir.mkdir(parents=True, exist_ok=True)
    m3u8_path = output_dir / "index.m3u8"

    # Команда ffmpeg для HLS
    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-vf", f"scale={width}:{height}",
        "-c:a", "aac", "-ar", "48000",
        "-c:v", "h264", "-profile:v", "main", "-crf", "20",
        "-g", "50", "-keyint_min", "50", "-sc_threshold", "0",
        "-b:v", bitrate, "-maxrate", bitrate, "-bufsize", "2M",
        "-hls_time", "4", "-hls_playlist_type", "vod",
        "-hls_segment_filename", str(output_dir / "segment_%03d.ts"),
        str(m3u8_path)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        log.info(f"HLS created: {m3u8_path}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"FFmpeg error: {e.stderr}")
        return False
    except FileNotFoundError:
        log.error("FFmpeg not found. Please install ffmpeg.")
        return False

@celery_app.task(name="process_video_hls")
def process_video_hls(video_id: str, original_filename: str):
    """
    Задача: создать HLS-версии для видео.
    """
    log.info(f"Processing HLS for video {video_id}")

    # Пути (используем настройку из config.py)
    base_path = Path(settings.local_storage_path)
    videos_path = base_path / "videos"
    input_path = videos_path / original_filename

    if not input_path.exists():
        log.error(f"Input file not found: {input_path}")
        return "error: input not found"

    # Создаём папку для HLS (например, media/hls/{video_id}/)
    hls_output_base = base_path / "hls" / video_id

    # Генерируем 360p и 720p
    success_360 = run_ffmpeg_hls(input_path, hls_output_base / "360p", 640, 360, "800k")
    success_720 = run_ffmpeg_hls(input_path, hls_output_base / "720p", 1280, 720, "2800k")

    if success_360 and success_720:
        log.info(f"HLS processing complete for {video_id}")
        return "success"
    else:
        log.error(f"HLS processing failed for {video_id}")
        return "error"