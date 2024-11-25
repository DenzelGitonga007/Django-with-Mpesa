from django.urls import path
from . import views
app_name = 'medi_app'

urlpatterns = [
    path('', views.home, name="home"), # home url
    path('about/', views.about, name="about"), # about url
    path('appointment/', views.appointment, name="appointment"), # appointment url
    path('show_appointments/', views.retrieve_appointments, name="show_appointments"), # url to show the appoinments
    path('delete/<int:id>', views.delete_appointment, name="delete_appointment"), # delete
    path('edit/<int:appointment_id>', views.update_appointment, name="update_appointment")
]