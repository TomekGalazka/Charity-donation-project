from django import forms
from django.forms import ModelForm

from . models import Donation


# class DonationForm(ModelForm):
#     class Meta:
#         model = Donation
#         fields = [
#             'quantity',
#             'categories',
#             'institution',
#             'address',
#             'phone_number',
#             'city',
#             'zip_code',
#             'pick_up_date',
#             'pick_up_time',
#             'pick_up_comment',
#         ]

class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    categories = forms.CharField()
    institution = forms.IntegerField()
    address = forms.CharField()
    phone_number = forms.IntegerField()
    city = forms.CharField()
    zip_code = forms.CharField()
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(widget=forms.Textarea)
