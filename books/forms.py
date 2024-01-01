from django import forms
from .models import review,RATINGS

class ReviewForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    ratings = forms.ChoiceField(choices=RATINGS)
    class Meta:
      model = review
      fields = ['user', 'book', 'body','ratings']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].disabled = True
        self.fields['book'].widget = forms.HiddenInput()
        self.fields['user'].disabled = True
        self.fields['user'].widget = forms.HiddenInput()

       