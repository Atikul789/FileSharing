from django.db import models
import datetime
from datetime import datetime

class File(models.Model):
    name = models.CharField(max_length=50, blank=True)
    file = models.FileField(blank=True)
    size = models.IntegerField(default=0, blank=True)
    hash = models.CharField(max_length=100, blank=True)
    blocking_status = models.BooleanField()  # blocking status for file
    request_accept = models.BooleanField()
    description = models.CharField(max_length=2000, blank=True)  # Optional file description
    url = models.CharField(max_length=255, blank=True)
    last_downloaded = models.DateTimeField(auto_now_add=False, blank=True, default=datetime.now())
    created = models.DateTimeField(auto_now_add=True)
