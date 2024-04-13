from django.shortcuts import render
from .models import Lodge

# Create your views here.
def lodge_list(request):
    lodges = Lodge.objects.all()
    return render(request, 'lodges/lodge_list.html', {'lodges': lodges})
