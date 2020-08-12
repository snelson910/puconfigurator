from django.db import models

class Customers(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sales_group = models.CharField(max_length=3, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    customer_account = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'
        verbose_name_plural = "customer"

    def __str__(self):
        return self.name