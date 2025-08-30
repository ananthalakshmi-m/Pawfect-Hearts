from django.shortcuts import render

def home_view(request):
    return render(request, 'home/home.html')

def loading_view(request):
    return render(request, "loading.html")