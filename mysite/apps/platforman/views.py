from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import platform

# Create your views here.

def index(request, template_name='platform_list.html'):
    """
    Return a list page of platforms.
    """
    object_list = platform.objects.order_by('name')
    return render_to_response(template_name,
                              {'object_list': object_list})

def detail(request, object_id, template_name='platform_detail.html'):
    """
    Return a detail page of platform.
    """
    object = get_object_or_404(platform, pk=object_id)
    return render_to_response(template_name,
                              {'object': object})