from django.contrib import admin

# Register your models here.
from .models import Requests,Votes

admin.site.register(Requests)
admin.site.register(Votes)
