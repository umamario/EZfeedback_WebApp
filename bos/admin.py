from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(CompanyPartner)
admin.site.register(Profile)