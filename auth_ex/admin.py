from django.contrib import admin

from charity_donation_app.models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type")


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "quantity", "address", "phone_number", "city", "zip_code", "pick_up_date",
        "pick_up_time", "pick_up_comment", "user"
    )
