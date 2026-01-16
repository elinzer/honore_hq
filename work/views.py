from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.http import HttpResponseRedirect

from households.mixins import HouseholdMixin, HouseholdAdminMixin
from households.models import HouseholdMembership
from locations.models import Unit
from .models import Task

User = get_user_model()


class TaskListView(HouseholdMixin, ListView):
    model = Task
    template_name = 'work/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        household = self.get_household()
        queryset = Task.objects.filter(household=household)

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by unit
        unit = self.request.GET.get('unit')
        if unit:
            queryset = queryset.filter(unit_id=unit)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Task.Status.choices
        context['units'] = Unit.objects.filter(household=self.get_household())
        context['current_status'] = self.request.GET.get('status', '')
        context['current_unit'] = self.request.GET.get('unit', '')
        return context


class TaskDetailView(HouseholdMixin, DetailView):
    model = Task
    template_name = 'work/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_pk'

    def get_queryset(self):
        return Task.objects.filter(household=self.get_household())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # User can edit if they created the task OR are an admin
        context['can_edit'] = (
            self.object.created_by == self.request.user or
            context['is_admin']
        )
        return context


class TaskCreateView(HouseholdMixin, CreateView):
    """All household members can create tasks."""
    model = Task
    template_name = 'work/task_form.html'
    fields = ['unit', 'title', 'description', 'status', 'priority', 'assigned_to', 'due_date']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        household = self.get_household()
        # Limit unit choices to this household
        form.fields['unit'].queryset = Unit.objects.filter(household=household)
        # Limit assigned_to to household members
        member_user_ids = HouseholdMembership.objects.filter(
            household=household,
            is_active=True
        ).values_list('user_id', flat=True)
        form.fields['assigned_to'].queryset = User.objects.filter(id__in=member_user_ids)
        return form

    def form_valid(self, form):
        form.instance.household = self.get_household()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('work:task_list', kwargs={'household_pk': self.kwargs['household_pk']})


class TaskUpdateView(HouseholdMixin, UpdateView):
    """Task creator or household admin can edit tasks."""
    model = Task
    template_name = 'work/task_form.html'
    fields = ['unit', 'title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
    pk_url_kwarg = 'task_pk'

    def get_queryset(self):
        return Task.objects.filter(household=self.get_household())

    def dispatch(self, request, *args, **kwargs):
        # Run parent dispatch first (checks login + membership)
        response = super().dispatch(request, *args, **kwargs)

        # Check if user can edit this task
        task = self.get_object()
        membership = self.get_membership()
        is_owner = task.created_by == request.user
        is_admin = membership.role == HouseholdMembership.Role.ADMIN

        if not (is_owner or is_admin):
            raise PermissionDenied("You can only edit tasks you created.")

        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        household = self.get_household()
        form.fields['unit'].queryset = Unit.objects.filter(household=household)
        # Limit assigned_to to household members
        member_user_ids = HouseholdMembership.objects.filter(
            household=household,
            is_active=True
        ).values_list('user_id', flat=True)
        form.fields['assigned_to'].queryset = User.objects.filter(id__in=member_user_ids)
        return form

    def get_success_url(self):
        return reverse('work:task_detail', kwargs={
            'household_pk': self.kwargs['household_pk'],
            'task_pk': self.object.pk
        })


class TaskStatusUpdateView(HouseholdMixin, View):
    """Quick status update - task creator or admin only."""

    def post(self, request, household_pk, task_pk):
        task = get_object_or_404(Task, pk=task_pk, household__pk=household_pk)

        # Check permission: owner or admin
        membership = self.get_membership()
        is_owner = task.created_by == request.user
        is_admin = membership.role == HouseholdMembership.Role.ADMIN

        if not (is_owner or is_admin):
            raise PermissionDenied("You can only update tasks you created.")

        new_status = request.POST.get('status')
        if new_status in dict(Task.Status.choices):
            task.status = new_status
            task.save(update_fields=['status', 'updated_at'])

        return HttpResponseRedirect(
            request.POST.get('next', reverse('work:task_list', kwargs={'household_pk': household_pk}))
        )
