from rest_framework import serializers
from .models import Progress,LearningSession

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
class LearningSessionSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(
        source="course.title",
        read_only=True
    )

    class Meta:
        model = LearningSession
        fields = [
            "id",
            "course",
            "course_title",
            "duration_minutes",
            "learning_date",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_course(self, course):
        if course and course.user != self.context["request"].user:
            raise serializers.ValidationError(
                "You can only select your own courses."
            )
        return course