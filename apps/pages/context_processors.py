from .models import Page

def pages(request):
    return {'shop_pages' : Page.objects.filter(menu_hide=False)}