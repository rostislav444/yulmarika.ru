from .models import FileCodes

def fron_files(request):
    context = {
        'front_files' :  FileCodes.objects.last()
    }
    context['favicon_ext'] = context['front_files'].favicon.name.split('.')[-1]
    return context