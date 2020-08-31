from django.db import models
from django.utils.text import slugify
from project import settings
from PIL import Image
from unidecode import unidecode
import os, PIL, io, json


class ImageField(models.ImageField):
    

    def delete(self, *args, **kwargs):
        print('DELETE')

    def get_path(self, instance):
        path = ""
        root = settings.MEDIA_ROOT
        for level in [instance._meta.app_label, instance._meta.model_name]:
            path += level + '/'
            if not os.path.isdir(root + path): 
                os.mkdir(root + path)
        return path

    def human_name(self, instance):
        instances = []
        inst = instance
        while True:
            instances.append(inst)
            if hasattr(inst,'parent'):
                inst = getattr(inst,'parent')
                continue
            break
        
        name_parts = [self.name]
        for inst in instances:
            if hasattr(inst, 'make_slug'):
                name_parts.append(inst.make_slug)
                break
            for attr in ['slug','name','title','code','category','create']:
                if hasattr(inst, attr):
                    attr = getattr(inst, attr)
                    if attr is not None:
                        name_parts.append(slugify(unidecode(str(attr))))
                        break
        name_parts.append(str(instance.pk))
        return name_parts


    def generate_filename(self, instance, filename, size=None):
        root = settings.MEDIA_ROOT
        path = self.get_path(instance)
        ext = filename.split('.')[-1]
        
        name_parts = self.human_name(instance)
        if size: 
            name_parts.append(size)
        filename = '-'.join(name_parts)
        
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
            return self.storage.generate_filename(filename)
    
        return f"{path}{filename}.{ext}"
        

    def save_form_data(self, instance, data):
        file = getattr(instance, self.attname)
        if not instance.pk:
            super(type(instance), instance).save()

        print(file != data)

        if file != data:
            if data is not None: 
                root = settings.MEDIA_ROOT
                if hasattr(instance, self.name + '_thmb'):
                    files = getattr(instance, self.name + '_thmb')
                    if files:
                        try: files = json.loads(files)
                        except: pass
                        for value in files.values():
                            try: os.remove(root + value)
                            except: pass
                        setattr(instance, self.name + '_thmb', {})

                size = (self.sizes['l'], self.sizes['l'])
                if data != False:
                    files = {}
                    filename = data.name
                    ext = filename.split('.')[-1]
                    image = PIL.Image.open(data).convert("RGB")
                    for key, value in self.sizes.items():
                        if key == 'l':
                            path = self.generate_filename(instance, filename)
                            image.thumbnail(size, PIL.Image.ANTIALIAS)
                            image_io = io.BytesIO()
                            image.save(image_io, format='JPEG')
                            data.file = image_io
                            files[key] = path
                        elif hasattr(instance, self.name + '_thmb'):
                            path = self.generate_filename(instance, filename, key)
                            image = PIL.Image.open(data).convert("RGB")
                            image.thumbnail((value, value), PIL.Image.ANTIALIAS)
                            image.save(settings.MEDIA_ROOT + path)
                            files[key] = path
                    image.close()
                    if hasattr(instance, self.name + '_thmb'):
                        files = json.dumps(files, indent=4, sort_keys=True, ensure_ascii=False)
                        setattr(instance, self.name + '_thmb', files)
        super(ImageField, self).save_form_data(instance, data)