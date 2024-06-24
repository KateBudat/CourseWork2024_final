from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    date_of_birth = models.DateField(blank=True, null=True)
    telephone_number = models.CharField(max_length=13)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        managed = False
        db_table = 'client'


class Master(models.Model):
    id_master = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    telephone_number = models.CharField(max_length=13)
    specialization = models.CharField(max_length=30)
    hire_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    dismissal_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        managed = False
        db_table = 'master'


@receiver(post_save, sender=Master)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        username = f'master{instance.id_master}'
        password = 'be@utyDemo24'
        custom_user = get_user_model().objects.create_user(
            username=username,
            password=password,
            role='master',  # Задайте роль за необхідністю
            master_id=instance,
            is_active=True,
            is_staff=True
        )

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    name_service = models.CharField(max_length=100)
    time_service = models.IntegerField()
    cost_service = models.DecimalField(max_digits=7, decimal_places=2)
    percent_for_master = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    type_service = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name_service}"
    class Meta:
        managed = False
        db_table = 'service'


class ServiceDetail(models.Model):
    id_service_details = models.AutoField(primary_key=True)
    master = models.ForeignKey(Master, models.DO_NOTHING, db_column='master')
    service = models.ForeignKey(Service, models.DO_NOTHING, db_column='service')
    deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'service_detail'
        unique_together = (('master', 'service'),)


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    name_material = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    barcode = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'material'


class Supplier(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_telephone = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.company_name}: {self.contact_person}"

    class Meta:
        managed = False
        db_table = 'supplier'


class Registration(models.Model):
    id_registration = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client')
    registration_date = models.DateField()
    start_time = models.TimeField()
    service_details = models.ForeignKey(ServiceDetail, models.DO_NOTHING, db_column='service_details')
    status = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'registration'


class Purchased_Material(models.Model):
    id_purchased_material = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING, db_column='supplier')
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    purchased_quantity = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()

    purchase_date = models.DateField(default=timezone.now, null=True)

    def save(self, *args, **kwargs):
        if self.purchase_date is None:
            self.purchase_date = timezone.now()  # Якщо дата покупки є null, встановлюємо сьогоднішню дату
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'purchased_material'


class Used_Material(models.Model):
    id_used_material = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    registration = models.ForeignKey(Registration, models.DO_NOTHING, db_column='registration')
    used_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'used_material'
        unique_together = (('material', 'registration'),)


class Write_Off_Material(models.Model):
    id_write_off_material = models.AutoField(primary_key=True)
    purchased_material = models.ForeignKey(Purchased_Material, models.DO_NOTHING, db_column='purchased_material')
    write_off_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    reason = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        if self.write_off_date is None:
            self.write_off_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'write_off_material'
