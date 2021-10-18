from django.db import models
from django.db.models.fields import EmailField
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, )
    email = models.EmailField(max_length=200)
    department = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    birth_date = models.DateField()

    def __str__(self):
        return self.name