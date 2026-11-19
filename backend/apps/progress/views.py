from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Progress,LearningSession
from .serializers import ProgressSerializer, LearningSessionSerializer

class ProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ["course"]

    def get_queryset(self):
        return Progress.objects.filter(
            user=self.request.user
        ).select_related("course")
class LearningSessionViewSet(viewsets.ModelViewSet):
    serializer_class = LearningSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningSession.objects.filter(
            user=self.request.user
        ).select_related("course")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)