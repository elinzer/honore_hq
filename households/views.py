from django.views.generic import TemplateView

from .models import HouseholdMembership


class HomeView(TemplateView):
    template_name = 'households/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = HouseholdMembership.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('household')
        return context
