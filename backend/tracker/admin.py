from django.contrib import admin
from .models import Category, Expense, Income, UserProfile

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Income)
