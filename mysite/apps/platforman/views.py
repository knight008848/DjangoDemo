from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import platform
from django.db import connection
import datetime, time
import csv

# Create your views here.

def index(request, template_name='platform_list.html'):
    """
    Return a list page of platforms.
    """
    p1 = request.GET.get('lob')
    kwargs = {
        # empty
    }
    
    if p1 is not None:
        kwargs ['lob'] = p1
        
    # platform list
    object_list = platform.objects.order_by('name').filter( **kwargs )
    
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)
    
    # menu
    lob_list = []
    cursor = connection.cursor()
    cursor.execute("""
            SELECT lob
            FROM platforman_platform
            Group by lob""")
    for row in cursor.fetchall():
        lob_list.append(row[0].upper())
        
    # result    
    return render_to_response(template_name,
                              {'object_list': object_list, 'lob_list': lob_list})

def detail(request, object_id, template_name='platform_detail.html'):
    """
    Return a detail page of platform.
    """
    object = get_object_or_404(platform, pk=object_id)
    return render_to_response(template_name,
                              {'object': object})

def output(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="platform.cfg"'

    object_list = platform.objects.order_by('name')
    gene_time = ';; File Date: ' + time.strftime("%A %b %d %Y", time.localtime())

    writer = csv.writer(response)
    writer.writerow([';;'])
    writer.writerow([';;###################################################################'])
    writer.writerow([';;# ScriptName: platform.ini'])
    writer.writerow([';;# Purpose:    Platform Configuration File used to FPP '])
    writer.writerow([';;-------------------------------------------------------------------'])
    writer.writerow([';;'])
    writer.writerow([';; [platform.<family-name>]'])
    writer.writerow([';; Model = <model number>       (Model number)'])
    writer.writerow([';; lob = XPS                    (Software Install Branded LOB)'])
    writer.writerow([';; pe_bits = 32 or 64            (32=Process starts 32-bit 64=Process starts 64-bit  used by FIDA)'])
    writer.writerow([';; type = BC or CSMB             (WBT enabled or not)'])
    writer.writerow([';; bios_sting = ***             (String in SMBIOS type 01 05)'])
    writer.writerow([';;'])
    writer.writerow([gene_time])
    writer.writerow([';;'])
    writer.writerow([';;###################################################################'])
    writer.writerow([';;'])

    for item in object_list:
        writer.writerow([])
        writer.writerow(['[platform.' + item.name.lower() + ']'])
        writer.writerow(['model = ' + item.model])
        writer.writerow(['lob = ' + item.lob])
        writer.writerow(['type = ' + item.type])
        writer.writerow(['pe_bits = ' + item.pebit])
        writer.writerow(['bios_string = ' + item.product])

    return response