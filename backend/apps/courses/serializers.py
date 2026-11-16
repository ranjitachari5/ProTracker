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
            "created_at",
            "progress",
            "status",
        ]
        read_only_fields = ["id", "created_at","status"]