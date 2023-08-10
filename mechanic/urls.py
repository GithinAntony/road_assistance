from django.urls import path
from . import views

app_name='mechanic'
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('list-complaints', views.complaints_list, name="complaints_list"),
    path('view-complaints/<int:id>', views.complaints_view, name="complaints_views"),
    path('add-messages/<int:id>/<int:id2>', views.add_messages, name="add_messages"),     
]
