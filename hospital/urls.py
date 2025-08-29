from django.urls import path
from .views import LoginView, RegisterView, create_patient_list, patient_details, create_doctor_list, doctor_details, map_doctor_patient, doctor_patient_mapping_list, delete_mappings

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    
    path('patients/', create_patient_list, name='patient_list'),
    path('patients/<int:pk>/', patient_details, name='patient'),
    
    path('doctors/', create_doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', doctor_details, name='doctor'),

    path('mapping/', doctor_patient_mapping_list, name='map_list'),
    path('mapping/<int:patient_id>/', map_doctor_patient, name='doctor_patient_mapping'),
    path('mapping/delete/<int:id>/', delete_mappings, name='delete_map'),
]