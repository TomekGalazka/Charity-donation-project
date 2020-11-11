from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
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
    type = models.CharField(max_length=7, choices=INSTITUTIONS)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name




