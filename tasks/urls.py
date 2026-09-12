from django.urls import path
from .views import CompleteTaskView, MyCompletionsView, TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<uuid:task_id>/complete/", CompleteTaskView.as_view(), name="task-complete"),
    path("my-completions/", MyCompletionsView.as_view(), name="my-completions"),
]
