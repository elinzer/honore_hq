from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Household, HouseholdMembership


class HouseholdMixin(LoginRequiredMixin):
    """Requires user to be an active member of the household."""

    _membership = None
    _household = None

    def get_household(self):
        """Get household from URL kwargs. Override if needed."""
        if self._household is None:
            self._household = get_object_or_404(Household, pk=self.kwargs['household_pk'])
        return self._household

    def get_membership(self):
        """Get the user's membership in the current household."""
        if self._membership is None:
            household = self.get_household()
            try:
                self._membership = HouseholdMembership.objects.get(
                    household=household,
                    user=self.request.user,
                    is_active=True
                )
            except HouseholdMembership.DoesNotExist:
                self._membership = False
        return self._membership if self._membership else None

    def dispatch(self, request, *args, **kwargs):
        # First check login
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check household membership BEFORE running view
        if not self.get_membership():
            raise PermissionDenied("You are not a member of this household.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        membership = self.get_membership()
        context['household'] = self.get_household()
        context['membership'] = membership
        context['is_admin'] = membership.role == HouseholdMembership.Role.ADMIN
        return context


class HouseholdAdminMixin(HouseholdMixin):
    """Requires user to be an ADMIN of the household."""

    def dispatch(self, request, *args, **kwargs):
        # First check login
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check membership and admin role BEFORE running view
        membership = self.get_membership()
        if not membership:
            raise PermissionDenied("You are not a member of this household.")
        if membership.role != HouseholdMembership.Role.ADMIN:
            raise PermissionDenied("You must be an admin to perform this action.")

        return super(HouseholdMixin, self).dispatch(request, *args, **kwargs)
