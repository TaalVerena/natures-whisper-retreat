from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def accounts_view(request):
    return HttpResponse("Testing Accounts http response.")