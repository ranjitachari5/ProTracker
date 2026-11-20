
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "platform",
            "course_url",
            "progress",
            "status",
            "created_at",
            "completed_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "completed_at",
        ]
