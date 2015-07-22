from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import gcfnote
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
    Send a file through Django by the id of record.  
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
    Send a file through Django by PO exists. 
    """
    object = get_object_or_404(gcfnote, po=ponumber)
    
    f =open(object.filepath)
    data = f.read()
    f.close()

    response = HttpResponse(data, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename="%s_GCF.XML" '% object.po
    response['Content-Length'] = os.path.getsize(object.filepath)
    return response