from django.urls import path

from . import views


app_name = 'charity_donation_app'

urlpatterns = [
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),
    # path('donation_choices/', views.donation_choices, name='donation_choices'),
    path('form_confirmation/', views.FormConfirmationView.as_view(), name='form-confirmation'),
    path('user_profile', views.UserView.as_view(), name='user-profile'),

]
