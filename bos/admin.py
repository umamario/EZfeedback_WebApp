from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Currency)
admin.site.register(Trade)
