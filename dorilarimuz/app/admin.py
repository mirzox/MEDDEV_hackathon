from django.contrib import admin

from .models import User, DoctorType, DoctorTypeChoices

admin.site.register(User)
admin.site.register(DoctorTypeChoices)
admin.site.register(DoctorType)
# admin.site.register(Client)
