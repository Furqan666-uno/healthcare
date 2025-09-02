from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient, Doctor, DoctorPatientMapping

User= get_user_model() # because we can't User model as it uses AbstractUser, so we need get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model= User
        fields= ('id', 'name', 'email', 'password')

    def create(self, validated_data):
        user= User.objects.create_user(name= validated_data['name'], email= validated_data['email'], password= validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer): # not ModelSerilazer here bcz we r not using class META here
    email= serializers.EmailField()
    password= serializers.CharField(write_only=True)

    def validate(self, data):
        user= authenticate(username=data['email'], password=data['password']) # since we r using email in place of username, so we map it accordingly
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        refresh= RefreshToken.for_user(user)

        return {'refresh':str(refresh), 'access':str(refresh.access_token)}
    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model= Patient
        fields= ['id', 'name', 'age', 'disease', 'created_at']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Doctor
        fields= ['id', 'name', 'yrs_of_experience', 'specialized_in']


class DoctorPatientMappingSerializer(serializers.ModelSerializer):
    doctor_name= serializers.CharField(source='doctor.name', read_only=True)
    patient_name= serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model= DoctorPatientMapping
        fields= ['id', 'doctor', 'doctor_name', 'patient_name', 'patient', 'mapping_done_on']

    # this validation prevents duplicate mapping of patient & doctor
    def validate(self, data):
        doctor= data['doctor'] # takes doctor from fields
        patient= data['patient'] # take patient from fields
        if DoctorPatientMapping.objects.filter(doctor=doctor, patient=patient).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return data
