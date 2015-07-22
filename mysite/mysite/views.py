from django.http import HttpResponse
import time

def hello(request):

    t = time.strftime('%A, %Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    return HttpResponse("Welcome to django world at %s." % t)