from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'household', 'unit', 'status', 'priority', 'assigned_to', 'due_date']
    list_filter = ['status', 'priority', 'household', 'unit']
    search_fields = ['title', 'description']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    raw_id_fields = ['created_by', 'assigned_to']
