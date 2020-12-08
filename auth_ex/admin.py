from django.contrib import admin

from auth_ex.models import User, UserManager
from charity_donation_app.models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "type")


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "quantity", "address", "phone_number", "city", "zip_code", "pick_up_date",
        "pick_up_time", "pick_up_comment", "institution", "user"
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_staff", "is_superuser")
