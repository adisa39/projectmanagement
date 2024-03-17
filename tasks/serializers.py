from rest_framework import serializers
from .models import Task, Project, User

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_project(self, obj):
        project_data = {
            'id': obj.project.pk,
            'title': obj.project.title,
            'description': obj.project.description,
            'created_at': obj.project.created_at,
            'updated_at': obj.project.updated_at,
            'task_count': obj.project.task_set.count(),
            'status_counts': {  # Count of tasks for each status
                'done': obj.project.task_set.filter(status='done').count(),
                'in_progress': obj.project.task_set.filter(status='in_progress').count(),
                'todo': obj.project.task_set.filter(status='todo').count(),
            }
        }
        return project_data  # Get 'project title', the field to display

    def get_assigned_to(self, obj):
        assigned_to_users = obj.assigned_to.all()  # Get all users assigned to the task
        users_data = []
        for user in assigned_to_users:
            user_data = {
                'id': user.pk,
                'username': user.username,
                # 'profile_picture': user.profile_picture.url if user.profile_picture else None
            }
            users_data.append(user_data)
        return users_data 