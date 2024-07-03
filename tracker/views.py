from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

# Create your views here.

def home(request):
    return render(request, 'tracker/home.html')
    