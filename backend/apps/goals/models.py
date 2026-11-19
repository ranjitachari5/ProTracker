
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Goal(models.Model):

    GOAL_TYPES = [
        ("course_target", "Course Target"),
        ("daily_learning", "Daily Learning"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals"
    )

    title = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    goal_type = models.CharField(
        max_length=20,
        choices=GOAL_TYPES
    )

    target_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    current_value = models.PositiveIntegerField(default=0)

    start_date = models.DateField()

    end_date = models.DateField()

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user}"
