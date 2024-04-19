from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Lodge


def lodge_list(request):
    """
    View function to display a list of lodges.
    Paginates the list to display a maximum of 3 lodges per page.
    """
    lodges_list = Lodge.objects.all().order_by('name')
    paginator = Paginator(lodges_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lodges/lodge_list.html', {'page_obj': page_obj})


def lodge_detail(request, pk):
    """
    View function to display details of a single lodge.
    """
    lodge = get_object_or_404(Lodge, pk=pk)
    return render(request, 'lodges/lodge_detail.html', {'lodge': lodge})
