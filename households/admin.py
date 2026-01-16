from django.contrib import admin
from .models import Household, HouseholdMembership


class HouseholdMembershipInline(admin.TabularInline):
    model = HouseholdMembership
    extra = 1


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    inlines = [HouseholdMembershipInline]


@admin.register(HouseholdMembership)
class HouseholdMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'household', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'household']
    search_fields = ['user__username', 'household__name']
