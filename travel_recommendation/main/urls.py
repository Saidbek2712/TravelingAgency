"""URL configuration for the main app."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('api/hotels/<int:dest_id>/', views.api_hotels, name='api_hotels'),
    path('api/book/', views.api_book, name='api_book'),
    path('booking/<int:booking_id>/pdf/', views.booking_pdf, name='booking_pdf'),
]
