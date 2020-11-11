from django.urls import path

from . import views

urlpatterns = [
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),

]
