from django.urls import include, path
from django.views.generic import TemplateView
from game.views import play
urlpatterns = [
    path("", play, name="play"),  # serves your game
]