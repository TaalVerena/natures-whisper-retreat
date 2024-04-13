from django.shortcuts import render, get_object_or_404
from .models import Lodge

# Create your views here.
def lodge_list(request):
    lodges = Lodge.objects.all()
    return render(request, 'lodges/lodge_list.html', {'lodges': lodges})

# Detail view for a single lodge
def lodge_detail(request, pk):
    lodge = get_object_or_404(Lodge, pk=pk)
    return render(request, 'lodges/lodge_detail.html', {'lodge': lodge})