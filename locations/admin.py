from django.contrib import admin
from .models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'household', 'unit_type', 'sort_order']
    list_filter = ['household', 'unit_type']
    search_fields = ['name', 'household__name']
    list_editable = ['sort_order']
