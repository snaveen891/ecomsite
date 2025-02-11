from django import forms
from .models import Order, CancellationRequest

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

class OrderCancellationForm(forms.ModelForm):
    class Meta:
        model = CancellationRequest
        fields = ['reason']


