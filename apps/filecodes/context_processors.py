from .models import FileCodes
import re

def fron_files(request):
    context = {
        'front_files' :  FileCodes.objects.last()
    }
    context['front_files'].phone = re.sub('[^0-9]', '', context['front_files'].phone) 
    context['favicon_ext'] = context['front_files'].favicon.name.split('.')[-1]
    return context