from django.db import models


class DummyData(models.Model):
    data = models.CharField(max_length=256)
