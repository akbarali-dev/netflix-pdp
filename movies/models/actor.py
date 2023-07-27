from django.db import models


class Actor(models.Model):
    MALE = 'male'
    FEMALE = 'female'

    GENDERS = (
        (MALE, MALE),
        (FEMALE, FEMALE)
    )

    name = models.CharField(max_length=155, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=155, choices=GENDERS, default=MALE)
