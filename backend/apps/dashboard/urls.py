
from django.urls import path
from .views import DashboardStatsView, CourseAnalyticsView

urlpatterns = [
    path("", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("analytics/", CourseAnalyticsView.as_view(), name="course-analytics"),
]
