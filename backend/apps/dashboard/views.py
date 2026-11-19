    
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.courses.models import Course
from apps.progress.models import Progress


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = Course.objects.filter(
            user=request.user
        ).aggregate(
            total_courses=Count("id"),
            completed_courses=Count(
                "id",
                filter=Q(status="completed")
            ),
            in_progress_courses=Count(
                "id",
                filter=Q(status="in_progress")
            ),
            not_started_courses=Count(
                "id",
                filter=Q(status="not_started")
            ),
            overall_progress=Avg("progress"),
        )

        stats["overall_progress"] = round(
            stats["overall_progress"] or 0
        )

        return Response(stats)


class CourseAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(user=request.user)

        # Course distribution
        distribution = courses.aggregate(
            completed=Count("id", filter=Q(status="completed")),
            in_progress=Count("id", filter=Q(status="in_progress")),
            not_started=Count("id", filter=Q(status="not_started")),
        )

        # Individual course progress
        course_progress = list(
            courses.values(
                "id",
                "title",
                "platform",
                "progress",
                "status",
            ).order_by("-created_at")
        )

        # Historical progress grouped by date
        history = list(
            Progress.objects.filter(user=request.user)
            .annotate(date=TruncDate("recorded_at"))
            .values("date")
            .annotate(
                average_progress=Avg("progress"),
                updates=Count("id"),
            )
            .order_by("date")
        )

        # Convert dates into JSON-friendly strings
        for item in history:
            item["date"] = item["date"].isoformat()

        overall_progress = courses.aggregate(
            average=Avg("progress")
        )["average"] or 0

        return Response({
            "distribution": distribution,
            "course_progress": course_progress,
            "history": history,
            "overall_progress": round(overall_progress),
        })
