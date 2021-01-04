from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from . forms import DonationForm
from . models import Donation, Institution, Category


class LandingPageView(View):
    """
    Landing page. Displays available institutions and summarizes donated bags and institutions.
    """
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
    """
    View processes data send with AJAX request.
        1. Returns institutions that only match certain categories (to display).
        2. Saves a new donation in database.
    """
    login_url = reverse_lazy('auth_ex:login')

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }

        return render(request, 'charity_donation_app/form.html', ctx)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            if request.POST.get('organization_pk', None) is not None:
                organization_pk = request.POST.get('organization_pk', None)
                organization_queryset = Institution.objects.filter(pk=organization_pk)
                organization = ""
                for item in organization_queryset:
                    organization += str(item)
                org_response = {'organization': organization}
                return JsonResponse(org_response)

            if request.POST.get('selected_categories_id', None) is not None:
                selected_categories_id = request.POST.get('selected_categories_id', None)
                selected_institutions_list = []

                for category_id in selected_categories_id:
                    category = Institution.objects.filter(categories=int(category_id))
                    for item in category:
                        selected_institutions = []
                        selected_institutions.append(item.pk)
                        selected_institutions.append(item.name)
                        selected_institutions.append(item.description)
                        selected_institutions_list.append(selected_institutions)

                response = {
                    'institutions': selected_institutions_list,
                }
                return JsonResponse(response)

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
    """
    User is redirected to this view after successful donation is made.
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation_app/form-confirmation.html')


class UserView(View):
    """
    View with user profile data. Display all donations made by logged in user.
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        user_donations = Donation.objects.filter(user=user)

        return render(request, 'charity_donation_app/profile.html', {'user_donations': user_donations})

