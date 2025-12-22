from django.shortcuts import render

# Create your views here.
def play(request):
    # authentication will later be here 
    return render(request, "game.html")

# here we will also have views for game session data tracking. 
# we will also build a model to store game session data.
# and we will build APIs to interact with the model.

