from django.db import models

class Contact(models.Model):
    country_code = models.CharField(max_length=5)  # +55
    first_name = models.CharField(max_length=100)  # first_name: Fábio
    last_name = models.CharField(max_length=100)  # last_name: Valeriano
    phone_number = models.CharField(max_length=15)  # phone_number: 35998782868
    is_favorite = models.BooleanField(default=False)  # is_favorite: true

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
