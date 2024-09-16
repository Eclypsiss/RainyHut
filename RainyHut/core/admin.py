from django.contrib import admin
from . import models

admin.site.register(models.Material)
admin.site.register(models.Order)
admin.site.register(models.Dishes)
admin.site.register(models.Table)
admin.site.register(models.Takeaway)
admin.site.register(models.Expense)
