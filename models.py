# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accumulators(models.Model):
    accum_size = models.CharField(max_length=-1, blank=True, null=True)
    part_number = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accumulators'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BellHousingSizes(models.Model):
    part_number = models.CharField(max_length=-1, blank=True, null=True)
    end_style = models.CharField(max_length=-1, blank=True, null=True)
    face_to_face = models.FloatField(blank=True, null=True)
    frame_size = models.CharField(max_length=-1, blank=True, null=True)
    coupling_size_pref = models.IntegerField(blank=True, null=True)
    max_coupling_size = models.IntegerField(blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'bell_housing_sizes'


class CouplingCodes(models.Model):
    code = models.CharField(max_length=-1, blank=True, null=True)
    sizes = models.CharField(max_length=-1, blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'coupling_codes'


class Customers(models.Model):
    name = models.CharField(max_length=-1, blank=True, null=True)
    sales_group = models.CharField(max_length=-1, blank=True, null=True)
    address = models.CharField(max_length=-1, blank=True, null=True)
    customer_account = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DampeningBars(models.Model):
    part_number = models.CharField(max_length=-1, blank=True, null=True)
    frame_sizes = models.CharField(max_length=-1, blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'dampening_bars'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Manifoldconfig(models.Model):
    manifold_id = models.IntegerField(blank=True, null=True)
    station = models.IntegerField(blank=True, null=True)
    fc_ports = models.CharField(max_length=-1, blank=True, null=True)
    fc_direct = models.CharField(max_length=-1, blank=True, null=True)
    cb_ports = models.CharField(max_length=-1, blank=True, null=True)
    red_ports = models.CharField(max_length=-1, blank=True, null=True)
    po_ports = models.CharField(max_length=-1, blank=True, null=True)
    rel_ports = models.CharField(max_length=-1, blank=True, null=True)
    red_checks = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manifoldconfig'


class Manifolds(models.Model):
    part_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    manifold_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manifolds'


class Motors(models.Model):
    motor_number = models.CharField(max_length=-1, blank=True, null=True)
    frame_size = models.CharField(max_length=-1, blank=True, null=True)
    shaft_length = models.FloatField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    voltage = models.CharField(max_length=-1, blank=True, null=True)
    coupling_max = models.CharField(max_length=-1, blank=True, null=True)
    coupling_code = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motors'


class Parts(models.Model):
    item_number = models.CharField(max_length=-1, blank=True, null=True)
    product_name = models.CharField(max_length=-1, blank=True, null=True)
    on_hand = models.IntegerField(blank=True, null=True)
    stockstatus = models.CharField(max_length=-1, blank=True, null=True)
    vendor = models.CharField(max_length=-1, blank=True, null=True)
    cost_each = models.FloatField(blank=True, null=True)
    list_price = models.FloatField(blank=True, null=True)
    leadtime = models.IntegerField(blank=True, null=True)
    saleslinedisc = models.CharField(max_length=-1, blank=True, null=True)
    purchlinedisc = models.CharField(max_length=-1, blank=True, null=True)
    costpricedate = models.DateField(blank=True, null=True)
    listpricedate = models.DateField(blank=True, null=True)
    contract_number = models.CharField(max_length=-1, blank=True, null=True)
    goto_item = models.CharField(max_length=-1, blank=True, null=True)
    gotomaxqty = models.CharField(max_length=-1, blank=True, null=True)
    csiaccount = models.CharField(max_length=-1, blank=True, null=True)
    csisalesrep = models.CharField(max_length=-1, blank=True, null=True)
    csicustname = models.CharField(max_length=-1, blank=True, null=True)
    csianniversarydate = models.DateField(blank=True, null=True)
    csilastreviewdate = models.DateField(blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'parts'


class Powerunitconfig(models.Model):
    unit_id = models.IntegerField(blank=True, null=True)
    p1_pressure = models.IntegerField(blank=True, null=True)
    p2_pressure = models.IntegerField(blank=True, null=True)
    p3_pressure = models.IntegerField(blank=True, null=True)
    p4_pressure = models.IntegerField(blank=True, null=True)
    p5_pressure = models.IntegerField(blank=True, null=True)
    a1_pressure = models.IntegerField(blank=True, null=True)
    a2_pressure = models.IntegerField(blank=True, null=True)
    a3_pressure = models.IntegerField(blank=True, null=True)
    a4_pressure = models.IntegerField(blank=True, null=True)
    a5_pressure = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    unitnotes = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'powerunitconfig'


class Powerunits(models.Model):
    unit_id = models.IntegerField(blank=True, null=True)
    part_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    customer = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'powerunits'


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=7, blank=True, null=True)
    created_on = models.DateTimeField()
    project_notes1 = models.CharField(max_length=-1, blank=True, null=True)
    project_notes2 = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class PumpDimensions(models.Model):
    pump_class = models.CharField(max_length=10, blank=True, null=True)
    pump_size = models.FloatField(blank=True, null=True)
    pump_suction = models.FloatField(blank=True, null=True)
    pump_suction_style = models.CharField(max_length=4, blank=True, null=True)
    pump_pressure = models.FloatField(blank=True, null=True)
    pump_pressure_style = models.CharField(max_length=4, blank=True, null=True)
    pump_case = models.FloatField(blank=True, null=True)
    pump_case_style = models.CharField(max_length=4, blank=True, null=True)
    pump_flange = models.CharField(max_length=2, blank=True, null=True)
    pump_shaft_length_key = models.FloatField(blank=True, null=True)
    pump_key_code = models.CharField(max_length=6, blank=True, null=True)
    pump_shaft_length_spline = models.FloatField(blank=True, null=True)
    pump_spline_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pump_dimensions'


class PumpNumbers(models.Model):
    pump_type = models.CharField(max_length=-1, blank=True, null=True)
    pump_size = models.CharField(max_length=-1, blank=True, null=True)
    control_type = models.CharField(max_length=-1, blank=True, null=True)
    part_number = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pump_numbers'


class Pumpcodes(models.Model):
    pump = models.CharField(max_length=-1, blank=True, null=True)
    pump_size = models.FloatField(blank=True, null=True)
    pump_suction = models.CharField(max_length=-1, blank=True, null=True)
    pump_suction_style = models.CharField(max_length=-1, blank=True, null=True)
    pump_pressure = models.CharField(max_length=-1, blank=True, null=True)
    pump_pressure_style = models.CharField(max_length=-1, blank=True, null=True)
    pump_case = models.CharField(max_length=-1, blank=True, null=True)
    pump_case_style = models.CharField(max_length=-1, blank=True, null=True)
    pump_flange = models.CharField(max_length=-1, blank=True, null=True)
    pump_shaft_length = models.FloatField(blank=True, null=True)
    pump_coupling_code = models.CharField(max_length=-1, blank=True, null=True)
    pump_shaft_style = models.CharField(max_length=-1, blank=True, null=True)
    pump_class = models.IntegerField(blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'pumpcodes'


class Reservoir(models.Model):
    reservoir_size = models.IntegerField(blank=True, null=True)
    reservoir_configuration = models.CharField(max_length=-1, blank=True, null=True)
    part_number = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservoir'


class SandwichNumbers(models.Model):
    function = models.CharField(max_length=-1, blank=True, null=True)
    d03 = models.CharField(max_length=-1, blank=True, null=True)
    d05 = models.CharField(max_length=-1, blank=True, null=True)
    d08 = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sandwich_numbers'


class Throughdrives(models.Model):
    rear_pump = models.CharField(max_length=-1, blank=True, null=True)
    a4vso250 = models.CharField(max_length=-1, blank=True, null=True)
    a4vso180 = models.CharField(max_length=-1, blank=True, null=True)
    a4vs0125 = models.CharField(max_length=-1, blank=True, null=True)
    a4vso71 = models.CharField(max_length=-1, blank=True, null=True)
    a4vso40 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso180_32 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso140_32 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso100_32 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso71_32 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso45_32 = models.CharField(max_length=-1, blank=True, null=True)
    a15vso280 = models.CharField(max_length=-1, blank=True, null=True)
    a15vso210 = models.CharField(max_length=-1, blank=True, null=True)
    a15vso175 = models.CharField(max_length=-1, blank=True, null=True)
    a15vso145 = models.CharField(max_length=-1, blank=True, null=True)
    a15vso110 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso140_31 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso100_31 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso71_31 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso45_31 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso28_31 = models.CharField(max_length=-1, blank=True, null=True)
    a10vso18_31 = models.CharField(max_length=-1, blank=True, null=True)
    azpf = models.CharField(max_length=-1, blank=True, null=True)
    azpg = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'throughdrives'


class WorkOrders(models.Model):
    customer_account = models.CharField(max_length=-1, blank=True, null=True)
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'work_orders'


class WorkOrdersTemp(models.Model):
    customer_account = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_orders_temp'
