from django.urls import path

from . import views


app_name = 'charity_donation_app'

urlpatterns = [
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),

]
