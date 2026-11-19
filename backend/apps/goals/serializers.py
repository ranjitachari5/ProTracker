
from rest_framework import serializers
from .models import Goal
from apps.courses.models import Course
from django.db.models import Sum
from django.utils import timezone
from apps.progress.models import LearningSession

class GoalSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    class Meta:
        model = Goal
        fields = [
            "id",
            "title",
            "description",
            "goal_type",
            "target_value",
            "current_value",
            "start_date",
            "end_date",
            "is_completed",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "current_value",
            "is_completed",
            "created_at",
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date cannot be before start date."
            })

        return attrs
    def get_current_value(self, obj):
        if obj.goal_type == "course_target":
            return Course.objects.filter(
            user=obj.user,
            status="completed",
            completed_at__date__gte=obj.start_date,
            completed_at__date__lte=obj.end_date,
        ).count()

        if obj.goal_type == "daily_learning":
            today = timezone.localdate()

            if not obj.start_date <= today <= obj.end_date:
                return 0

            total = LearningSession.objects.filter(
            user=obj.user,
            learning_date=today,
        ).aggregate(
            total=Sum("duration_minutes")
        )

            return total["total"] or 0

        return obj.current_value


    def get_is_completed(self, obj):
        if obj.goal_type != "course_target":
            return obj.is_completed

        return self.get_current_value(obj) >= obj.target_value
