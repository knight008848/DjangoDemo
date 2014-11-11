import os, sys
#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = project + os.sep + "mysite"

sys.stdout = sys.stderr     #put log to error.log in Apache

print apache_configuration, project
sys.path.append(workspace)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()