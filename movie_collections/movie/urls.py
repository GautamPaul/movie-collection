from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user),
    path('movies/', views.movies),
    path('collection/', views.collection),
    path('collection/<uuid:id>/', views.collection_detail),
    path('request-count/', views.request_count),
    path('request-count/reset/', views.request_count_reset)
]
