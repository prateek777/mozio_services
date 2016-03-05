from __future__ import unicode_literals

from django.db import models

# Create your models here.

#########################
"""Current DB structure in mongoDB for Providers:
	
	name: Name of the Service Provider(COMPULSARY)
    email: The email address of the service provider(COMPULSARY). Also has a unique index specified.
    phone_number: The phone number of the service provider(COMPULSARY)
    language: The preferred language for the service provider(COMPULSARY)
    currency: The preferred currency for the service provider(COMPULSARY)

"""