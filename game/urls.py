from django.urls import include, path
from django.views.generic import TemplateView
from game.views import play, dashboard
urlpatterns = [
    path("play", play, name="play"),  # serves your game
    path("dashboard", dashboard, name="dashboard"),  # serves the dashboard)
]