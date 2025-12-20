from django.core.management.base import BaseCommand
from safety_checker.models import YouTubeChannel, YouTubeVideo, VideoAnalysis

class Command(BaseCommand):
    help = 'Seeds the database with GARM benchmark data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding benchmark data...')
        
        # Reset State
        VideoAnalysis.objects.all().delete()
        YouTubeVideo.objects.all().delete()
        YouTubeChannel.objects.all().delete()

        # 1. Benchmark: Brand Safe
        tech_channel = YouTubeChannel.objects.create(
            channel_id='UC_TECH_BENCH',
            name='Tech Reviewer Daily',
            description='Benchmark for Safe Content'
        )
        tech_video = YouTubeVideo.objects.create(
            video_id='VID_TECH_001',
            title='Flagship Device Review',
            description='Standard tech review content.',
            channel=tech_channel
        )
        VideoAnalysis.objects.create(
            video=tech_video,
            overall_score=0.98,
            risk_tier=VideoAnalysis.RiskTier.SAFE,
            is_brand_safe=True,
            garm_scores={'garm_adult': 0.0, 'garm_hate_speech': 0.0, 'garm_violence': 0.01},
            detected_flags=[],
            analysis_summary="Verified Safe.",
            processor_version="v2.0-stable"
        )

        # 2. Benchmark: High Risk (Violative)
        edgy_channel = YouTubeChannel.objects.create(
            channel_id='UC_RISK_BENCH',
            name='Edgy Vlogger',
            description='Benchmark for Unsafe Content'
        )
        edgy_video = YouTubeVideo.objects.create(
            video_id='VID_RISK_001',
            title='Prank gone wrong',
            description='Contains harassment.',
            channel=edgy_channel
        )
        VideoAnalysis.objects.create(
            video=edgy_video,
            overall_score=0.15,
            risk_tier=VideoAnalysis.RiskTier.HIGH,
            is_brand_safe=False,
            garm_scores={'garm_hate_speech': 0.85, 'garm_violence': 0.6},
            detected_flags=['hate_speech', 'harassment'],
            analysis_summary="Violates GARM Safety Standards.",
            processor_version="v2.0-stable"
        )

        # 3. Benchmark: Contextual (News)
        news_channel = YouTubeChannel.objects.create(
            channel_id='UC_NEWS_BENCH',
            name='Global News Network',
            description='Benchmark for Contextual Risk'
        )
        news_video = YouTubeVideo.objects.create(
            video_id='VID_NEWS_001',
            title='Global Unrest Coverage',
            description='Political coverage.',
            channel=news_channel
        )
        VideoAnalysis.objects.create(
            video=news_video,
            overall_score=0.6,
            risk_tier=VideoAnalysis.RiskTier.MEDIUM,
            is_brand_safe=True,
            garm_scores={'garm_violence': 0.3, 'garm_sensitive_social_issues': 0.8},
            detected_flags=['political_conflict'],
            analysis_summary="Contextual Risk: News event.",
            processor_version="v2.0-stable"
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded 3 benchmark channels.'))
