from celery import shared_task
from .models import YouTubeChannel, YouTubeVideo, VideoAnalysis
import random
import time

@shared_task
def analyze_channel_task(channel_name):
    """
    Performs asynchronous analysis of a YouTube channel.
    Simulates fetching video metadata, running GARM safety models,
    and persisting results to PostgreSQL.
    """
    print(f"[{channel_name}] Starting asynchronous analysis...")
    
    # Simulate API latency and inference time
    time.sleep(5) 
    
    channel, _ = YouTubeChannel.objects.get_or_create(
        name=channel_name,
        defaults={
            'channel_id': f"UC_{random.randint(1000, 9999)}",
            'description': f"Automated description for {channel_name}"
        }
    )

    video = YouTubeVideo.objects.create(
        video_id=f"VID_{random.randint(10000, 99999)}",
        title=f"Latest Upload from {channel_name}",
        description="Analyzed content.",
        channel=channel
    )

    # Simulate GARM Model Inference
    # In production, this would call an external specific model or API
    is_safe = random.random() > 0.3 
    
    if is_safe:
        risk_tier = VideoAnalysis.RiskTier.SAFE
        overall_score = random.uniform(0.85, 0.99)
        garm_scores = {k: 0.0 for k in ['garm_adult', 'garm_hate_speech', 'garm_violence']}
        detected_flags = []
        summary = "Content is verified as brand safe."
    else:
        risk_tier = VideoAnalysis.RiskTier.HIGH
        overall_score = random.uniform(0.1, 0.5)
        garm_scores = {
            'garm_adult': round(random.random(), 2),
            'garm_hate_speech': round(random.random(), 2),
            'garm_violence': round(random.random(), 2)
        }
        detected_flags = [k for k, v in garm_scores.items() if v > 0.5]
        summary = f"High risk content detected. Triggered flags: {', '.join(detected_flags)}"

    VideoAnalysis.objects.create(
        video=video,
        overall_score=round(overall_score, 2),
        risk_tier=risk_tier,
        is_brand_safe=is_safe,
        garm_scores=garm_scores,
        detected_flags=detected_flags,
        analysis_summary=summary,
        processor_version="StreamSentry-Worker-v1"
    )
    
    print(f"[{channel_name}] Analysis complete. Saved to DB.")
    return f"Processed {channel_name}"
