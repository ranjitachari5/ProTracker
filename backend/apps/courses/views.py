from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.progress.models import Progress
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["platform", "status"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "progress", "title"]
    ordering = ["-created_at"]
    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save(user=self.request.user)

        Progress.objects.create(
        user=self.request.user,
        course=course,
        progress=course.progress,
        )
    def perform_update(self, serializer):
         previous_progress = self.get_object().progress

         course = serializer.save()

         if course.progress != previous_progress:
            Progress.objects.create(
            user=self.request.user,
            course=course,
            progress=course.progress,
        )