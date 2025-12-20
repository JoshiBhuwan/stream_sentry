from django.shortcuts import render
from .models import YouTubeChannel, VideoAnalysis
from .tasks import analyze_channel_task

def get_channel_safety_report(channel_name):
    """
    Retrieves existing analysis or dispatches a background task.
    """
    try:
        channel = YouTubeChannel.objects.filter(name__icontains=channel_name).first()
        
        if not channel:
            # Dispatch async analysis task
            analyze_channel_task.delay(channel_name)
            return {
                'status': 'Processing',
                'message': f"Analyzing '{channel_name}'...",
                'css_class': 'processing',
                'refresh_needed': True
            }

        last_analysis = VideoAnalysis.objects.filter(video__channel=channel).order_by('-processed_at').first()

        if not last_analysis:
             return {
                'status': 'Processing',
                'message': 'Report generation in progress...',
                'css_class': 'processing',
                'refresh_needed': True
            }

        risk_class = 'safe' if last_analysis.risk_tier == 'SAFE' else 'unsafe'

        return {
            'status': last_analysis.get_risk_tier_display(),
            'message': last_analysis.analysis_summary,
            'css_class': risk_class,
            'garm_scores': last_analysis.garm_scores,
            'overall_score': last_analysis.overall_score
        }

    except Exception:
         return {
            'status': 'Error',
            'message': "An unexpected system error occurred.",
            'css_class': 'review'
        }

def index(request):
    result = None
    channel_name = request.POST.get('channel_name') or request.GET.get('channel_name', '')
    
    if channel_name:
        result = get_channel_safety_report(channel_name)
    
    return render(request, 'safety_checker/index.html', {
        'result': result,
        'channel_name': channel_name
    })
