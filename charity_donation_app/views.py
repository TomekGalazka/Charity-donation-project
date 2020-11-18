from django.shortcuts import render
from django.views import View

from . models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        all_donations = Donation.objects.all()
        quantity_counter = 0
        for donation in all_donations:
            quantity_counter += donation.quantity
        institutions = all_donations.distinct('institution').count()

        charitable_trust_institutions = Institution.objects.filter(type='Trust')
        non_gov_institutions = Institution.objects.filter(type='Non-gov')
        local_institutions = Institution.objects.filter(type='Local')

        list_1 = []

        for institution in charitable_trust_institutions:
            for category in institution.categories.values_list():
                list_1.append(category[1])
                institution_categories = ", ".join(list_1)

        context = {
            'quantity_counter': quantity_counter,
            'institution_counter': institutions,
            'Found': charitable_trust_institutions,
            'Non_gov': non_gov_institutions,
            'Local': local_institutions,
        }
        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form.html')

