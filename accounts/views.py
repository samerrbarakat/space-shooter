from django.shortcuts import render , redirect 
from .forms import CustomUserCreationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  
        # here it uses the already built in login view/ 
        else:
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})