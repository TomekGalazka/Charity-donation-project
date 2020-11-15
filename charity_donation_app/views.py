from django.shortcuts import render
from django.views import View

from . models import Donation


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        all_donations = Donation.objects.all()
        quantity_counter = 0
        institutions_list = []
        for donation in all_donations:
            quantity_counter += donation.quantity
            if donation.institution not in institutions_list:
                institutions_list.append(donation.institution)
        institutions = len(institutions_list)

        context = {
            'quantity_counter': quantity_counter,
            'institution_counter': institutions
        }
        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form.html')

