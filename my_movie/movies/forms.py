from django.forms import ModelForm
from .models import Reviews

class ReviewsForm(ModelForm):
    """Форма с отзывами"""
    class Meta:
        model = Reviews
        fields = ['name', 'text', 'email']
