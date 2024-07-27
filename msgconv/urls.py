from django.urls import path
from .views import LandingView

urlpatterns = [
    path('', LandingView.as_view(), name='index'),
    path('upload/', LandingView.as_view(), name='index'),
]