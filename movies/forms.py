from django import forms
#from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Revive, Rating, RatingStars


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    #captcha = ReCaptchaField()

    class Meta:
        model = Revive
        fields = ('name', 'text', 'email')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }


class RatingForm(forms.ModelForm):
    """Форма рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)
