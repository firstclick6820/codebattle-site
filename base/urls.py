from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name="register_page"),
    path('user/<uuid:id>/', views.user_page, name="profile"),
    path('event/<uuid:id>/', views.event_page, name='event_page'),
    path('event/<uuid:id>/register', views.event_registration, name="event_registration"),
    path('account/', views.user_account_page, name='user_account'),
    path('project_submission/<uuid:id>/', views.project_submission, name='project_submission'),
    path('update_submission/<uuid:id>/', views.update_submission, name='update_submission'),
    
]
