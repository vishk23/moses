from django.db import models

class BeatHealth(models.Model):
    last_heartbeat = models.DateTimeField()

