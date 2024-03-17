from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import Project
from .serializers import ProjectSerializer


def index(request):
    return render(request, 'projects/index.html')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.prefetch_related('task_set').filter(task__status=status)
        return queryset
