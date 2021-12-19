from django.urls import path
from authapp import views as authapp

app_name = 'authapp'


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('verify/<email>/<key>/', authapp.verify, name='verify'),
    path('api/reg/', authapp.RegistrationAPIView.as_view(), name='APIreg'),
    path('api/log/', authapp.LoginAPIView.as_view(), name='APIlog'),
    path('api/load/', authapp.LoadAPIView.as_view(), name='APIload'),
]

