from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('view/', views.view, name='view'),
    path('update/', views.update, name='update'),
    path('stats/', views.stats, name='stats')
]