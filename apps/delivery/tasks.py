from apps.delivery.models import Delivery
from celery import shared_task


@shared_task
def test_calculator(*args, **kwargs):
    d = Delivery()
    d.test_api()
