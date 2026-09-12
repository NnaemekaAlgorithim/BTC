import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models


class Task(models.Model):
    class TaskType(models.TextChoices):
        WATCH_VIDEO = "watch_video", "Watch Video"
        CLICK_LINK = "click_link", "Click Link"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    url = models.URLField(help_text="Link or video URL the user must visit")
    btc_reward = models.DecimalField(
        max_digits=30,
        decimal_places=11,
        default=Decimal("0.00000000001"),
    )
    is_active = models.BooleanField(default=True)
    # None means unlimited; set a number to cap total completions across all users
    max_completions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def completion_count(self):
        return self.completions.count()

    @property
    def is_exhausted(self):
        if self.max_completions is None:
            return False
        return self.completions.count() >= self.max_completions


class UserTaskCompletion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_completions",
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completions")
    btc_earned = models.DecimalField(max_digits=30, decimal_places=11)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # one completion per user per task
        unique_together = ("user", "task")

    def __str__(self):
        return f"{self.user} — {self.task}"
