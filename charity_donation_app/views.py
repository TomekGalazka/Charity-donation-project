from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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


class AddDonationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth_ex:login')

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions
        }

        return render(request, 'charity_donation_app/form.html', ctx)

    def post(self, request, *args, **kwargs):
        quantity = self.request.POST.get('bags', None)
        categories = self.request.POST.get_list('categories', None)
        institution = self.request.POST.get('organization', None)
        address = self.request.POST.get('address', None)
        phone_number = self.request.POST.get('phone_number', None)
        city = self.request.POST.get('city', None)
        zip_code = self.request.POST.get('postcode', None)
        pick_up_date = self.request.POST.get('date', None)
        pick_up_time = self.request.POST.get('time', None)
        pick_up_comment = self.request.POST.get('more_info', None)

        user = request.user

        add_donation = Donation.objects.create(
            quantity=quantity,
            categories=categories,
            institution=institution,
            address=address,
            city=city,
            phone_number=phone_number,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )
        add_donation.user.add(user)
        return redirect(reverse_lazy('charity_donation_app:form_confirmation'))


class FormConfirmationView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form_confirmation.html')


def donation_choices(request, *args, **kwargs):
    if request.method == 'GET':
        bags = request.GET.get('bags', None)
        organization_id = request.GET.get('organization', None)
        city = request.GET.get('city', None)
        postcode = request.GET.get('postcode', None)
        date = request.GET.get('date', None)
        time = request.GET.get('time', None)
        more_info = request.GET.get('more_info', None)

        organization = Institution.objects.get(pk=organization_id)

        data = {
            'worki': bags,
            'organizacja': organization.name,
            'miasto': city,
            'kod_pocztowy': postcode,
            'twoja_data': date,
            'czas': time,
            'informacje': more_info
        }
        response = JsonResponse(data)
        return response


class UserView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        user_donations = Donation.objects.filter(user=user)

        return render(request, 'charity_donation_app/profile.html', {'user_donations': user_donations})
