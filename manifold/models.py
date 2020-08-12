from django.db import models

class Manifold(models.Model):
    manifold_id = models.IntegerField(blank=True, null=True)
    part_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'manifolds'

class Manifoldconfig(models.Model):
    manifold_id = models.IntegerField(blank=True, null=True)
    station = models.IntegerField(blank=True, null=True)
    fc_ports = models.CharField(max_length=255, blank=True, null=True)
    fc_direct = models.CharField(max_length=255, blank=True, null=True)
    cb_ports = models.CharField(max_length=255, blank=True, null=True)
    red_ports = models.CharField(max_length=255, blank=True, null=True)
    po_ports = models.CharField(max_length=255, blank=True, null=True)
    rel_ports = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'manifoldconfig'

class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=7, blank=True, null=True)
    created_on = models.DateTimeField()
    project_notes1 = models.TextField(blank=True, null=False)
    project_notes2 = models.TextField(blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'projects'

class Customers(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sales_group = models.CharField(max_length=3, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    customer_account = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'