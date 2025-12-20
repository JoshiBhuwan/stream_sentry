from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import YouTubeVideo
# from .tasks import analyze_channel_task 

# Note: We currently handle analysis dispatch explicitly via views.py
# and the Celery worker. Automatic signaling on model creation is disabled
# to prevent recursion loops (Worker creates Video -> Signal fires -> ...).

# @receiver(post_save, sender=YouTubeVideo)
# def trigger_video_analysis(sender, instance, created, **kwargs):
#     if created:
#         pass
