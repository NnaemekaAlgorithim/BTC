from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, UserTaskCompletion
from .serializers import TaskSerializer, UserTaskCompletionSerializer


class TaskListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tasks = Task.objects.filter(is_active=True).order_by("-created_at")
        serializer = TaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)


class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, is_active=True)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if task.is_exhausted:
            return Response(
                {"detail": "This task has reached its maximum number of completions."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if UserTaskCompletion.objects.filter(user=request.user, task=task).exists():
            return Response(
                {"detail": "You have already completed this task."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        completion = UserTaskCompletion.objects.create(
            user=request.user,
            task=task,
            btc_earned=task.btc_reward,
        )

        request.user.btc_balance += task.btc_reward
        request.user.save(update_fields=["btc_balance"])

        serializer = UserTaskCompletionSerializer(completion)
        return Response(
            {
                "detail": "Task completed! BTC credited to your balance.",
                "btc_earned": str(task.btc_reward),
                "new_balance": str(request.user.btc_balance),
                "completion": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class MyCompletionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        completions = (
            request.user.task_completions
            .select_related("task")
            .order_by("-completed_at")
        )
        serializer = UserTaskCompletionSerializer(completions, many=True)
        return Response(serializer.data)
