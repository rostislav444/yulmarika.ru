from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'


    # def ready(self):
    #     from apps.core.models import ModelImages
    #     from django.db import models

    #     def getModule(app_name=None):
    #         module = __import__('apps')
    #         path = app_name + '.admin'
    #         for directory in path.split('.'):
    #             module = getattr(module, directory)
    #         return module
        
    #     for model in ModelImages.__subclasses__():
    #         print(model)
    #         model.Meta.abstract = True
    #         model._meta.abstract = True
    #         app_name =  model._meta.app_label
    #         module = getModule(app_name)
            # model.Meta.abstract = True
            # fields_to_create = {}
            # image_field = models.ImageField(editable=True, null=True, blank=True)
            # char_field =  models.CharField(editable=True, max_length=1000, null=True, blank=True)

            # for field in model._meta.get_fields(include_hidden=False):
            #     if field.__class__.__name__ == 'ImageField':
            #         for size in model.sizes.keys():
            #             setattr(model, field.name + '_' + size, image_field)
            #         setattr(model, field.name + '_url', char_field)
            
                   
           