# tasks.py
import datetime
from datetime import datetime, timedelta

import celery

from .models import File


@celery.decorators.periodic_task(
    run_every=datetime.timedelta(minutes=5))  # here we assume we want it to be run every 5 mins
def delete_file_data():
    for record in File.objects.all():
        # I assumed here that date_time is time when your object was created
        time_elapsed =  record.last_downloaded - datetime.now()
        if time_elapsed > timedelta(days=15):
            record.delete()
