from django.urls import path
from . import views

urlpatterns = [
    path('', views.facility_list, name='facility_list'),
    path('facility/<int:pk>/', views.facility_detail, name='facility_detail'),
    path('facility/<int:pk>/book/', views.book_facility, name='book_facility'),
    path('bookings/', views.booking_list, name='booking_list'), 
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'), 
]
