
from django.db import models
from django.conf import settings
from apps.courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Progress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="progress_history"
    )

    progress = models.PositiveIntegerField(
    validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ]
)

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        constraints = [
        models.CheckConstraint(
            condition=Q(progress__gte=0) & Q(progress__lte=100),
            name="progress_between_0_and_100",
        )
    ]

    def __str__(self):
        return f"{self.course.title} - {self.progress}%"

class LearningSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_sessions"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_sessions"
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    learning_date = models.DateField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-learning_date", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(duration_minutes__gte=1),
                name="learning_session_duration_positive",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.duration_minutes} minutes"
