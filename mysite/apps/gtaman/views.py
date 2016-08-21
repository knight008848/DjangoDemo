from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import gcfnote
from django.db import connection
from django.db.models import Q
import os

def detail(request, object_id, template_name='detail.html'):
    """
    Return a detail page of GCF.
    """
    object = get_object_or_404(gcfnote, pk=object_id)
    return render_to_response(template_name,
                              {'object': object})

def download_id(request, object_id):
    """
    Send a file through Django without loading the whole file into               
    memory at once. The FileWrapper will turn the file object into an            
    iterator for chunks of 8KB.  
    """
    object = get_object_or_404(gcfnote, pk=object_id)
    
    f =open(object.filepath)
    data = f.read()
    f.close()

    response = HttpResponse(data, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename="%s_GCF.XML" '% object.po
    response['Content-Length'] = os.path.getsize(object.filepath)
    return response

def download_po(request, ponumber):
    """
    Send a file through Django without loading the whole file into               
    memory at once. The FileWrapper will turn the file object into an            
    iterator for chunks of 8KB.  
    """
    object = get_object_or_404(gcfnote, po=ponumber)
    
    f =open(object.filepath)
    data = f.read()
    f.close()

    response = HttpResponse(data, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename="%s_GCF.XML" '% object.po
    response['Content-Length'] = os.path.getsize(object.filepath)
    return response
    
def index(request, template_name='list.html'):
    """
    Return a list page of platforms.
    """
    model = request.GET.get('model')
    os = request.GET.get('os')
    level = request.GET.get('level')
    region = request.GET.get('region')
    s = request.GET.get('search')
    search = u''
    
    kwargs = {
        # empty
    }

    url = ''
    
    if model is not None and model != 'All Model':
        kwargs ['family'] = model
        url = urllink(url, 'model=' + model)
    
    if os is not None and os != 'All OSVersion':
        kwargs ['OSV'] = os
        url = urllink(url, 'os=' + os)
        
    if level is not None and level != 'All Level':
        kwargs ['level'] = level
        url = urllink(url, 'level=' + level)

    if region is not None:
        kwargs ['region'] = region
        url = urllink(url, 'region=' + region)
        
    if s != None:
        search = s
        url = urllink(url, 'search=' + search)

    object_list = gcfnote.objects.filter( **kwargs ).filter(
        Q(sdr__icontains = search) | Q(po__icontains = search)
        ).order_by('-timestamp')
    
    paginator = Paginator(object_list, 50)
    page = request.GET.get('page')
    
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        object_list = paginator.page(paginator.num_pages)
    
    page_range_list = []
    for item in paginator.page_range:
        if item == 1 or item == paginator.num_pages:
            page_range_list.append(item)
        elif item == int(page):
            page_range_list.append(item)
        elif item >= int(page) -2 and item <= int(page) + 2:
            page_range_list.append(item)
        else:
            if page_range_list[-1] != 0:
                page_range_list.append(0)
    
    model_list = []
    cursor = connection.cursor()
    cursor.execute("""
            SELECT family
            FROM gtaman_gcfnote
            Group by family""")
    for row in cursor.fetchall():
        model_list.append(row[0].upper())
        
    os_list = []
    cursor = connection.cursor()
    cursor.execute("""
            SELECT OSV
            FROM gtaman_gcfnote
            Group by OSV""")
    for row in cursor.fetchall():
        os_list.append(row[0].upper())
        
    level_list = []
    cursor = connection.cursor()
    cursor.execute("""
            SELECT level
            FROM gtaman_gcfnote
            Group by level""")
    for row in cursor.fetchall():
        level_list.append(row[0].upper())
        
    region_list = []
    cursor = connection.cursor()
    cursor.execute("""
            SELECT region
            FROM gtaman_gcfnote
            Group by region""")
    for row in cursor.fetchall():
        region_list.append(row[0].upper())
        
    # result    
    return render_to_response(template_name, locals())


def getKwargs(data={}):
	kwargs = {}
	for (k , v)  in data.items() :
		if v is not None and v != u'' :
			kwargs[k] = v          
	return kwargs

def urllink(url, st):
	if url =='':
		url = st
	else:
		url = url + '&' + st
	return url
