from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
@login_required
def play(request):
    return render(request, "game.html")

@login_required
def dashboard(request):
    return render(request, "landing.html")
# here we will also have views for game session data tracking. 
# we will also build a model to store game session data.
# and we will build APIs to interact with the model.

