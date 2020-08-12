from django import forms
from .models import Motors, Pumpcodes, Reservoir

class HPForm(forms.ModelForm):
    hp = forms.ModelChoiceField(queryset=Motors.objects.distinct('hp').order_by('hp'), label="Horsepower", empty_label="Select...", to_field_name="hp")
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

class FrameForm(forms.ModelForm):
    frames = forms.ModelChoiceField(queryset=Motors.objects.distinct('frame_size'))
    class Meta:
        model=Motors
        fields = [
            "frames",
        ]

class ReservoirForm(forms.ModelForm):
    reservoirs = forms.ModelChoiceField(queryset=Reservoirs.objects.order_by('reservoir_size', 'id', lavel="Reservoir", empty_label="Select...", to_field_name="reservoir")
    class Meta:
        model=Reservoirs
        fields = [
            "reservoirs",
        ]