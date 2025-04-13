from django.urls import path
from .views import CreateVideoView, HealthCheckView


urlpatterns = [
    path('create/', CreateVideoView.as_view(), name='video'),
    path('health/', HealthCheckView.as_view(), name='health'),
]