from django.db import models

class user(models.Model):
    sales_group = models.CharField(max_length=3)
