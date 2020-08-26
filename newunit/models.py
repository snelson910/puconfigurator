from django.db import models

class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=7, blank=True, null=True)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'projects'

class Motors(models.Model):
    motor_number = models.CharField(max_length=255, blank=True, null=False)
    frame_size = models.CharField(max_length=255, blank=True, null=True)
    shaft_length = models.FloatField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    voltage = models.CharField(max_length=255, blank=True, null=True)
    coupling_max = models.CharField(max_length=255, blank=True, null=True)
    coupling_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motors'
    
    def __str__(self):
        return u'{0}, {1}'.format(self.hp, self.frame_size)

class Pumpcodes(models.Model):
    pump = models.CharField(max_length=255, blank=True, null=True)
    pump_size = models.CharField(max_length=255, blank=True, null=True)
    pump_suction = models.CharField(max_length=255, blank=True, null=True)
    pump_suction_style = models.CharField(max_length=255, blank=True, null=True)
    pump_pressure = models.CharField(max_length=255, blank=True, null=True)
    pump_pressure_style = models.CharField(max_length=255, blank=True, null=True)
    pump_case = models.CharField(max_length=255, blank=True, null=True)
    pump_case_style = models.CharField(max_length=255, blank=True, null=True)
    pump_flange = models.CharField(max_length=255, blank=True, null=True)
    pump_shaft_length = models.FloatField(blank=True, null=True)
    pump_coupling_code = models.CharField(max_length=255, blank=True, null=True)
    pump_shaft_style = models.CharField(max_length=255, blank=True, null=True)
    pump_class = models.FloatField(blank=True, null=True)
    rear_pump = models.CharField(max_length=255, blank=True, null=True)
    front_pump = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pumpcodes'

    def __str__(self):
        return u'{0}'.format(self.pump)

class BellHousingSizes(models.Model):
    part_number = models.CharField(max_length=255, blank=True, null=True)
    end_style = models.CharField(max_length=255, blank=True, null=True)
    face_to_face = models.FloatField(blank=True, null=True)
    frame_size = models.CharField(max_length=255, blank=True, null=True)
    max_coupling_size = models.IntegerField(blank=True, null=True)
    coupling_size_pref = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bell_housing_sizes'

class CouplingCodes(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    sizes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupling_codes'

class Reservoir(models.Model):
    reservoir_size = models.CharField(max_length=255, blank=True, null=True)
    reservoir_configuration = models.CharField(max_length=255, blank=True, null=True)
    part_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservoir'
    def __str__(self):
        return u'{0} Gallons , {1}'.format(self.reservoir_size, self.reservoir_configuration)

class Throughdrives(models.Model):
    rear_pump = models.CharField(max_length=255, blank=True, null=True)
    a4vso250 = models.CharField(max_length=255, blank=True, null=True)
    a4vso180 = models.CharField(max_length=255, blank=True, null=True)
    a4vso125 = models.CharField(max_length=255, blank=True, null=True)
    a4vso71 = models.CharField(max_length=255, blank=True, null=True)
    a4vso40 = models.CharField(max_length=255, blank=True, null=True)
    a10vso180_32 = models.CharField(max_length=255, blank=True, null=True)
    a10vso140_32 = models.CharField(max_length=255, blank=True, null=True)
    a10vso100_32 = models.CharField(max_length=255, blank=True, null=True)
    a10vso71_32 = models.CharField(max_length=255, blank=True, null=True)
    a10vso45_32 = models.CharField(max_length=255, blank=True, null=True)
    a15vso280 = models.CharField(max_length=255, blank=True, null=True)
    a15vso210 = models.CharField(max_length=255, blank=True, null=True)
    a15vso175 = models.CharField(max_length=255, blank=True, null=True)
    a15vso145 = models.CharField(max_length=255, blank=True, null=True)
    a15vso110 = models.CharField(max_length=255, blank=True, null=True)
    a10vso140_31 = models.CharField(max_length=255, blank=True, null=True)
    a10vso100_31 = models.CharField(max_length=255, blank=True, null=True)
    a10vso71_31 = models.CharField(max_length=255, blank=True, null=True)
    a10vso45_31 = models.CharField(max_length=255, blank=True, null=True)
    a10vso28_31 = models.CharField(max_length=255, blank=True, null=True)
    a10vso18_31 = models.CharField(max_length=255, blank=True, null=True)
    azpf = models.CharField(max_length=255, blank=True, null=True)
    azpg = models.CharField(max_length=255, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'throughdrives'