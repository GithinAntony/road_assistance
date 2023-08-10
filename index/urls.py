from django.urls import path
from . import views

app_name='index'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('service', views.service, name='service'),
    path('why', views.why, name='why'),
    path('contact-us', views.contact_us, name='contact_us'),
    ]
