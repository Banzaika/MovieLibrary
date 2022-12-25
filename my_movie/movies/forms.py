from django.forms import ModelForm, ModelChoiceField, RadioSelect
from .models import Reviews, Rating, RatingStar

class ReviewsForm(ModelForm):
    """Форма с отзывами"""
    class Meta:
        model = Reviews
        fields = ['name', 'text', 'email']

class RatingForm(ModelForm):
    """Форма добавления рейтинга"""
    star = ModelChoiceField(queryset=RatingStar.objects.all(), widget=RadioSelect, empty_label=None)

    class Meta:
        model = Rating
        fields = ("star", )