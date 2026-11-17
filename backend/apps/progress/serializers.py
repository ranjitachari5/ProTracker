from rest_framework import serializers
from .models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(
        source="course.title",
        read_only=True
    )

    class Meta:
        model = Progress
        fields = [
            "id",
            "course",
            "course_title",
            "progress",
            "recorded_at",
        ]
        read_only_fields = fields