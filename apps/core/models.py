from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
from project import settings
from django.utils import timezone
from PIL import Image
from unidecode import unidecode
import os, PIL, io, json, jsonfield
from django.utils import timezone, dateformat
import gzip
from sh import pg_dump


class BackUpDB(models.Model):
    name = models.CharField(max_length=300, blank=True, verbose_name="Имя файла")
    path = models.CharField(max_length=300, blank=True, verbose_name="Адрес файла")
    date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата дампа базы")
    url =  models.CharField(max_length=1000, blank=True, null=True, verbose_name="Сслыка")
    loaded = models.BooleanField(default=False, verbose_name="Загружен в облако")

    def dump_db(self):
        self.name = 'backup_' + dateformat.format(timezone.now(), 'Y-m-d_H-i-s')
        path = f'media/backup/{self.name}.sql'
        with gzip.open(path, 'wb') as f:
            pg_dump('yulmarika', _out=f)
        self.path = path
        super(BackUpDB, self).save()

    def server_load(self):
        return ''

    def save(self):
        self.dump_db()
        super(BackUpDB, self).save()


# Models
class NameSlug(models.Model):
    name =  models.CharField(max_length=300, blank=False, verbose_name="Название")
    slug =  models.CharField(max_length=320, blank=True, null=True, verbose_name="Иденитификатор", editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(unidecode(self.name))
        super(NameSlug, self).save()

IMAGES_SIZES = {
    'l':2400,
    'm':1200,
    's':480,
    'xs':80
}

class ModelImages(models.Model):
    

    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

    def get_path(self):
        path = ""
        root = settings.MEDIA_ROOT
        for level in [self._meta.app_label, self._meta.model_name]:
            path += level + '/'
            if not os.path.isdir(root + path): 
                os.mkdir(root + path)
        return path
    
    def human_name(self, field_name):
        instances = []
        inst = self
        while True:
            instances.append(inst)
            if hasattr(inst,'parent'):
                inst = getattr(inst,'parent')
                continue
            break

        name_parts = [field_name]
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
        
        if not self.id:
            last_obj = type(self).objects.last()
            if last_obj:
                self.id = last_obj.id + 1
            else:
                self.id = 1
        
        name_parts.append('id'+str(self.id))
        return '__'.join(name_parts)


    def delete_old(self, thmbs, dirpath, filename):
        for address, dirs, files in os.walk(settings.MEDIA_ROOT + dirpath):
            for file in files:
                if filename in file:
                    try: os.remove(address+file)
                    except: pass
        for path in thmbs.values():
            try: os.remove(path)
            except: pass
    

    def save(self):
        for field in self._meta.get_fields():
            # Get image field
            if field.get_internal_type() == 'FileField' and field.attr_class.__name__ == 'ImageFieldFile':
                image_field = getattr(self, field.name)
                thmbs_name = field.name + '_thmb'
                thmbs = getattr(self,thmbs_name)
                # Check old image
                try:    old_image_path = thmbs['l']
                except: old_image_path = None
                # If image changed
                if image_field.name and image_field.name != old_image_path:
                    dirpath = self.get_path()
                    filename = self.human_name(field.name)
                    filepath = dirpath + filename
                    ext = image_field.name.split('.')[-1]
                    self.delete_old(thmbs, dirpath, filename)

                    thmbs = {}
                    image = PIL.Image.open(image_field.file).convert("RGB")
                    image_io = io.BytesIO()
                    image.save(image_io, format='JPEG')
                    image_field.name = filepath + '.' + ext
                    super(ModelImages, self).save()
                 
                    for key, size in IMAGES_SIZES.items():
                        if key == 'l':  path = filepath + '.' + ext
                        else:           path = filepath + '_' + key + '.' + ext
                        media_path = settings.MEDIA_ROOT + path
                        image = PIL.Image.open(image_io)
                        image.thumbnail((size, size), PIL.Image.ANTIALIAS)
                        image.save(media_path)
                        thmbs[key] = path
                    setattr(self, thmbs_name, thmbs)
        super(ModelImages, self).save()


    @property
    def imgs(self):
        data = {}
        for field in self._meta.get_fields():
            if '_thmb' in field.name:
                field_data = getattr(self, field.name)
                if field_data:
                    field_name = field.name.replace('_thmb','')
                    data[field_name] = {}
                    if not isinstance(field_data, dict):
                        field_data = json.loads(field_data)
                    for key, value in field_data.items():
                        data[field_name][key] = settings.MEDIA_URL + value
        return data
             
    def pre_delete(self):
        for field in self._meta.get_fields():
            if field.get_internal_type() == 'FileField' and field.attr_class.__name__ == 'ImageFieldFile':
                image_field = getattr(self, field.name)
                thmbs_name = field.name + '_thmb'
                thmbs = getattr(self, thmbs_name)
                dirpath = self.get_path()
                filename = self.human_name(field.name)
                self.delete_old(thmbs, dirpath, filename)
                
                   
                       
# Signals
@receiver(pre_delete)
def make_pre_delete(sender, instance, signal, *args, **kwargs):
    if hasattr(instance, 'pre_delete'):
        instance.pre_delete()


