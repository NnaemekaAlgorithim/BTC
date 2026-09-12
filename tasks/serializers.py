from rest_framework import serializers

from .models import Task, UserTaskCompletion


class TaskSerializer(serializers.ModelSerializer):
    completion_count = serializers.IntegerField(read_only=True)
    already_completed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "task_type",
            "url",
            "btc_reward",
            "is_active",
            "max_completions",
            "completion_count",
            "already_completed",
            "created_at",
        ]

    def get_already_completed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return UserTaskCompletion.objects.filter(user=request.user, task=obj).exists()
        return False


class UserTaskCompletionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source="task.title", read_only=True)
    task_type = serializers.CharField(source="task.task_type", read_only=True)

    class Meta:
        model = UserTaskCompletion
        fields = ["id", "task_title", "task_type", "btc_earned", "completed_at"]
