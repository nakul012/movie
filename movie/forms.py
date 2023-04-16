from django import forms
from .models import Movie


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


class MovieOmdbForm(forms.Form):
    title = forms.CharField(max_length=200)
