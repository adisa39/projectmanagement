from rest_framework import serializers
from .models import Project
from tasks.models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    todo_count = serializers.SerializerMethodField()
    in_progress_count = serializers.SerializerMethodField()
    done_count = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_tasks(self, obj):
        tasks = obj.task_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data

    def get_tasks_count(self, obj):
        return obj.task_set.count()

    def get_todo_count(self, obj):
        return obj.task_set.filter(status='todo').count()

    def get_in_progress_count(self, obj):
        return obj.task_set.filter(status='in_progress').count()

    def get_done_count(self, obj):
        return obj.task_set.filter(status='done').count()

    def get_assigned_to(self, obj):
        assigned_to_users = obj.task_set.values_list('assigned_to', flat=True).distinct()
        users = User.objects.filter(pk__in=assigned_to_users)
        return [{'id': user.id, 'username': user.username} for user in users]