from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name="register"), # register
    path('login/', views.login_view, name="login"), # login
]