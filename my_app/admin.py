from django.contrib import admin
from .models import CustomUser, Category

admin.site.register(CustomUser)
admin.site.register(Category)
