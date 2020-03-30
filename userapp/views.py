from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import CustomRegForm

# Create your views here.
def register(request):
    if request.method == "POST":
        regform = CustomRegForm(request.POST)
        if regform.is_valid():
            regform.save()
            messages.success(request,"New User Account Created , Login To Start!")
            return redirect ("register")
    else:
        regform = CustomRegForm() 
    return render(request,"register.html",{"regform":regform})