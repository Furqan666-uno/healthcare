from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username= None
    email= models.EmailField(unique=True)
    name= models.CharField(max_length=100)

    USERNAME_FIELD= 'email' # this replace username
    REQUIRED_FIELDS= [] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Patient(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    name= models.CharField(max_length=100)
    age= models.IntegerField()
    disease= models.CharField(max_length=255, blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} is a {self.age}years old patient'
    

class Doctor(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctors')
    name= models.CharField(max_length=100)
    specialized_in= models.CharField(max_length=100)
    yrs_of_experience= models.IntegerField(default=0)

    def __str__(self):
        return f'Dr.{self.name} specialized in {self.specialized_in}, has {self.yrs_of_experience}of experience'
    

class DoctorPatientMapping(models.Model):
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    mapping_done_on= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ('patient', 'doctor') # to make sure every mapping is unique 

    def __str__(self):
        return f'{self.patient.name} is mapped to {self.doctor.name}'