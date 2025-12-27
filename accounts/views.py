from django.shortcuts import render , redirect 
from .forms import CustomUserCreationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})