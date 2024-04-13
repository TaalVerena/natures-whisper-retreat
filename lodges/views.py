from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Lodge

# Create your views here.
def lodge_list(request):
    lodges_list = Lodge.objects.all().order_by('name')
    paginator = Paginator(lodges_list, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    return render(request, 'lodges/lodge_list.html', {'page_obj': page_obj})

# Detail view for a single lodge
def lodge_detail(request, pk):
    lodge = get_object_or_404(Lodge, pk=pk)
    return render(request, 'lodges/lodge_detail.html', {'lodge': lodge})