from django.contrib import admin

from .models import Customers

class CustomersAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "customer_account", "sales_group")

admin.site.register(Customers, CustomersAdmin)