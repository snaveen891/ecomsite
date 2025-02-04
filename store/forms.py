from .models import ProductReview
from django import forms

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(6)])
        }

class SearchForm(forms.Form):
    query = forms.CharField()