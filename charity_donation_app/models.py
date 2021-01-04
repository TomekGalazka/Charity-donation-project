from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    """
    Model represents a category that binds with different institutions. Different donations only apply to institutions
    with certain categories.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    """
    Model represents institution to which a donation can be made.
    """
    FOUND = 'Trust'
    NON_GOV = 'Non-gov'
    LOCAL = 'Local'
    INSTITUTIONS = [
        (FOUND, 'Charitable Trust'),
        (NON_GOV, 'Non-governmental organization'),
        (LOCAL, 'Local charity')
    ]

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=7, choices=INSTITUTIONS, default=FOUND)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    Model represents a donation that can be made to certain institution. Each donation needs to have a personalized
    data.
    """
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)





