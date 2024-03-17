from django.contrib import admin
from .models import Project
from tasks.models import Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0  # Number of extra forms to display


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_editable = ['description',]
    list_filter = ['created_at', 'updated_at']
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    inlines = [TaskInline]


admin.site.register(Project, ProjectAdmin)
