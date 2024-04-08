from django.shortcuts import render
from .models import LodgeOverview

# Create your views here.

def home_view(request):
    lodges = LodgeOverview.objects.all()
    return render(request, 'home/index.html', {'lodges': lodges})