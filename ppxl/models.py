from django.db import models

# Create your models here.

# A model that allows CRUD for the MPTP dictionary


class MPTP(models.Model):

    # Stops list of items being displayed in admin interface as "MPTPs", which is an incorrect plural
    class Meta:
        verbose_name_plural = 'MPTP'
        ordering = ['name']

    name = models.CharField(
        max_length=100,
        verbose_name="Item name")
    itemdesc = models.CharField(
        max_length=255,
        verbose_name="POS Works Description")
    mptp_applies = models.BooleanField(default=True)
    mptp = models.FloatField(
        verbose_name="Maximum Price to Patient",
        blank=True,
        null=True)
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date added")
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Last modified")
    link = "Edit"

    def __str__(self):
        return self.name
