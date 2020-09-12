from celery import shared_task
from .models import BackUpDB

@shared_task
def dump_db(*args, **kwargs):
    db = BackUpDB()
    db.save()
    return {'dumped' : db.loaded}




