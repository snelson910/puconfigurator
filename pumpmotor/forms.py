from django import forms
from newunit.models import Motors, Pumpcodes, Reservoir

class HPForm(forms.ModelForm):
    hp = forms.ModelChoiceField(queryset=Motors.objects.distinct('hp').order_by('hp'), label="Motor", empty_label="Select...", to_field_name="hp")
    class Meta:
        model=Motors
        fields = [
            "hp",
        ]

class PumpForm(forms.ModelForm):
    pumps = forms.ModelChoiceField(queryset=Pumpcodes.objects.order_by('pump_class', 'pump_size'),label="Pump", empty_label="Select...", to_field_name="pump")
    class Meta:
        model=Pumpcodes
        fields = [
            "pumps",
        ]