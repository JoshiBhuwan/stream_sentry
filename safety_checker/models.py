from django.db import models
from django.contrib.postgres.fields import ArrayField

class YouTubeChannel(models.Model):
    """
    Represents a YouTube Channel entity.
    """
    channel_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class YouTubeVideo(models.Model):
    """
    Represents a specific video upload.
    """
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    channel = models.ForeignKey(YouTubeChannel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VideoAnalysis(models.Model):
    """
    Stores the GARM Suitability Analysis results for a video.
    Includes granular scoring for brand safety categories.
    """
    class RiskTier(models.TextChoices):
        SAFE = 'SAFE', 'Brand Safe'
        LOW = 'LOW', 'Low Risk'
        MEDIUM = 'MEDIUM', 'Medium Risk'
        HIGH = 'HIGH', 'High Risk'

    video = models.OneToOneField(YouTubeVideo, on_delete=models.CASCADE, related_name='analysis')
    
    # High-Level Metrics
    overall_score = models.FloatField(help_text="0.0 (Unsafe) to 1.0 (Safe)")
    risk_tier = models.CharField(max_length=20, choices=RiskTier.choices, default=RiskTier.HIGH)
    is_brand_safe = models.BooleanField(default=False)
    
    # Detailed GARM Breakdown (e.g., {"violence": 0.05, "adult": 0.0})
    garm_scores = models.JSONField(default=dict, help_text="Detailed scores per GARM category")
    
    # Targeted 'Flags' for immediate filtering
    detected_flags = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    analysis_summary = models.TextField()
    processed_at = models.DateTimeField(auto_now_add=True)
    processor_version = models.CharField(max_length=50, default="v1.0")

    def __str__(self):
        return f"Analysis for {self.video.title}: {self.risk_tier}"

class ChannelAnalysis(models.Model):
    """
    Aggregated analysis for a channel based on its recent videos.
    """
    channel = models.OneToOneField(YouTubeChannel, on_delete=models.CASCADE)
    average_suitability_score = models.FloatField()
    overall_risk_tier = models.CharField(max_length=20)
    last_analyzed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel.name} - {self.overall_risk_tier}"
    