import os
import PIL
from unidecode import unidecode
from project import settings
from django.utils.text import slugify
from project import settings
import shutil
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os
import binascii



def tempImagePath(instance, filename):
    ext = filename.split('.')[-1]
    return str(binascii.hexlify(os.urandom(16))) +'.' + ext


def imageResize(self, fieldname, name):
    # Globals
    root = settings.MEDIA_ROOT
    image = getattr(self, fieldname)
    response =   {'l' : None, 's' : None, 'url' : None}
    imageSizes = {'l' : 1920, 's' : 96}

    def set_response(self):
        image_l = getattr(self, fieldname)
        image_s = getattr(self, fieldname + '_s')
        setattr(image_l, 'name', response['l'])
        setattr(image_s, 'name', response['s'])
        setattr(self, fieldname + '_url', response['l']) 
        return self


    if image.name is None or os.path.exists(root + image.name) == False: 
        return set_response(self)
    
    
    
    ext =  str(image.name.split('.')[-1]).lower()

    
    def get_path(self):
        path = ''
        for level in [self._meta.app_label, self._meta.model_name]:
            path += level + '/'
            if not os.path.isdir(root + path): 
                os.mkdir(root + path)
        return path


    def add_png_alpha(image):
        background = PIL.Image.new("RGBA", image.size, (0,0,0,0))
        background.paste(image)
        return background
        

    def make_thumbs(self, image):
        path = get_path(self)
        for size, res in imageSizes.items():
            filename =  f'{path}{fieldname}__{name}-{size}.{ext}'
            resize_image = PIL.Image.open(image)
            if ext == 'png': 
                image = add_png_alpha(image)
            resize_image.thumbnail((res, res), PIL.Image.ANTIALIAS)
            resize_image.save(root + filename, quality=100)
            resize_image.close()
            response[size] = filename


    
    
    # Remove old image
    # try: 
    #     image_l = getattr(self, fieldname)
    #     os.remove(image_l.path)
    #     image_s = getattr(self, fieldname + '_s')
    #     os.remove(image_s.path)
    # except: pass

    # Curent admin loaded image path
    # try: old_path = image.path
    # except: pass

    # Ckeck extantion and make thumbs
    if ext in ['jpg', 'jpeg', 'png']:
        make_thumbs(self, image.path)
    else: pass

    # Remove initial image from temp path
    # try: os.remove(old_path)
    # except: pass

   
    return set_response(self)





