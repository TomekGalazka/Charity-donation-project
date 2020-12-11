from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from . forms import DonationForm
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

        if request.is_ajax():
            organization_pk = request.POST['organization_pk']
            organization_queryset = Institution.objects.filter(pk=organization_pk)
            organization = ""
            for item in organization_queryset:
                organization += str(item)
            org_response = {'organization': organization}
            return JsonResponse(org_response)

        form = DonationForm(request.POST)
        if form.is_valid():
            categories_string = form.cleaned_data.get('categories')
            quantity = form.cleaned_data.get('quantity')
            organization_id = form.cleaned_data.get('institution')
            city = form.cleaned_data.get('city')
            address = form.cleaned_data.get('address')
            phone = form.cleaned_data.get('phone_number')
            date = form.cleaned_data.get('pick_up_date')
            time = form.cleaned_data.get('pick_up_time')
            more_info = form.cleaned_data.get('pick_up_comment')
            post_code = form.cleaned_data.get('zip_code')

            split_categories_string = categories_string.split(", ")

            categories_ids = [int(category_id) for category_id in split_categories_string]

            organization = Institution.objects.get(pk=organization_id)
            categories = Category.objects.filter(pk__in=categories_ids)

            user = request.user

            add_donation = Donation.objects.create(
                quantity=quantity,
                institution=organization,
                address=address,
                city=city,
                phone_number=phone,
                zip_code=post_code,
                pick_up_date=date,
                pick_up_time=time,
                pick_up_comment=more_info,
                user=user
            )
            for category in categories:
                add_donation.categories.add(category)

            data = {'mission_completed': 'All is ok!'}
            response = JsonResponse(data)
            return response


class FormConfirmationView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form-confirmation.html')


class UserView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        user_donations = Donation.objects.filter(user=user)

        return render(request, 'charity_donation_app/profile.html', {'user_donations': user_donations})

