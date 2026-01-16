from django.contrib import admin
from django.urls import include, path

from households.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('households/<int:household_pk>/tasks/', include('work.urls')),
]
