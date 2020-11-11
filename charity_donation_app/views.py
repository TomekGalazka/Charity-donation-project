from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class AddDonationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form.html')

