from django.urls import path
from . import views

app_name='public'
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('search-mechanic', views.search_mechanic, name="search_mechanic"),
    path('search-mechanic-view/<int:id>', views.search_mechanic_view, name="search_mechanic_view"),
    path('add-messages/<int:id>/<int:id2>', views.add_messages, name="add_messages"),                 
 ]
