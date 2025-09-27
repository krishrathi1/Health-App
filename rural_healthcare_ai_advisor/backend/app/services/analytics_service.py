class AnalyticsService:
    def get_overview_metrics(self) -> dict:
        return {
            "total_consultations": 0,
            "triage_distribution": {"emergency": 0, "urgent": 0, "homecare": 0},
            "avg_response_minutes": 0,
        }


_global_analytics_service: AnalyticsService | None = None


def get_analytics_service() -> AnalyticsService:
    global _global_analytics_service
    if _global_analytics_service is None:
        _global_analytics_service = AnalyticsService()
    return _global_analytics_service

