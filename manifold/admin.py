from django.contrib import admin

from .models import Manifold, Manifoldconfig

class ManifoldAdmin(admin.ModelAdmin):
    list_display = ("manifold_id", "part_number", "quantity")

class ManifoldconfigAdmin(admin.ModelAdmin):
    list_display = ("manifold_id", "station", "fc_ports", "fc_direct", "cb_ports", "red_ports", "po_ports", "rel_ports")

admin.site.register(Manifold, ManifoldAdmin)
admin.site.register(Manifoldconfig, ManifoldconfigAdmin)