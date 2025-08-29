from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, PatientSerializer, DoctorSerializer, DoctorPatientMappingSerializer
from .models import Patient, Doctor, DoctorPatientMapping


class RegisterView(CreateAPIView):
    serializer_class= RegisterSerializer


class LoginView(GenericAPIView):
    serializer_class= LoginSerializer

    def post(self, request):
        login_data= self.get_serializer(data=request.data)
        if login_data.is_valid():
            return Response(login_data.validated_data, status=status.HTTP_200_OK)
        return Response({'message':'Something went wrong...'}, status=status.HTTP_401_UNAUTHORIZED)
    

# ----------------------------------------PATIENTS-------------------------------------------


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def create_patient_list(request):
    if request.method=='GET':
        patients= Patient.objects.filter(user=request.user)
        patient_list= PatientSerializer(patients, many=True)
        return Response(patient_list.data)
    
    elif request.method=='POST':
        new_patient= PatientSerializer(data=request.data)
        if new_patient.is_valid():
            new_patient.save(user=request.user)
            return Response(new_patient.data, status=status.HTTP_201_CREATED)
        return Response(new_patient.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def patient_details(request, pk):
    try:
        patient= Patient.objects.get(pk=pk, user=request.user)
    except Patient.DoesNotExist:
        return Response({'error':'patient not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        get_patient= PatientSerializer(patient)
        return Response(get_patient.data)
    
    elif request.method=='PUT':
        update_patient= PatientSerializer(patient, data=request.data)
        if update_patient.is_valid():
            update_patient.save()
            return Response(update_patient.data)
        return Response(update_patient.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        patient.delete()
        return Response({'message':'Patient deleted from database.'}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------------------DOCTORS----------------------------------    


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def create_doctor_list(request):
    if request.method=='GET':
        doctors= Doctor.objects.all()
        get_doctors= DoctorSerializer(doctors, many=True)
        return Response(get_doctors.data)
    
    elif request.method=='POST':
        new_doctor= DoctorSerializer(data=request.data)
        if new_doctor.is_valid():
            new_doctor.save(user=request.user)
            return Response(new_doctor.data, status=status.HTTP_201_CREATED)
        return Response(new_doctor.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def doctor_details(request, pk):
    try:
        doctors= Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response({'message':'Doctor not found...'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        get_doctor= DoctorSerializer(doctors)
        return Response(get_doctor.data)
    
    elif request.method=='PUT':
        update_doctor= DoctorSerializer(doctors, data=request.data, partial=True)
        if update_doctor.is_valid():
            update_doctor.save()
            return Response(update_doctor.data)
        return Response(update_doctor.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        doctors.delete()
        return Response({'message':"Doctor's data is deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

# -----------------------------------------MAPPING-------------------------------------    


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def doctor_patient_mapping_list(request):
    if request.method=='GET':
        map= DoctorPatientMapping.objects.all()
        get_map= DoctorPatientMappingSerializer(map, many=True)
        return Response(get_map.data)
    
    elif request.method=='POST':
        add_map= DoctorPatientMappingSerializer(data=request.data)
        if add_map.is_valid():
            doctor= add_map.validated_data['doctor']
            patient= add_map.validated_data['patient']
            # to prevent saving duplicate mapping of patient and doctor
            if DoctorPatientMapping.objects.filter(doctor=doctor, patient=patient).exists():
                return Response({'message':'This doctor is already assigned to this patient.'}, status=status.HTTP_400_BAD_REQUEST)
            add_map.save()
            return Response(add_map.data, status=status.HTTP_201_CREATED)
        return Response(add_map.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def map_doctor_patient(request, patient_id):
    try:
        patient= Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return Response({'message':'Patient not found...'}, status=status.HTTP_404_NOT_FOUND)
    
    map= DoctorPatientMapping.objects.filter(patient=patient)
    get_map= DoctorPatientMappingSerializer(map, many=True)
    return Response(get_map.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_mappings(self, request, id):
    try:
        to_delete_map= DoctorPatientMapping.objects.get(pk=id)
    except DoctorPatientMapping.DoesNotExist:
        return Response({'message':'Mapping not found...'}, status=status.HTTP_404_NOT_FOUND)
    
    to_delete_map.delete()
    return Response({'message':'The map is deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
