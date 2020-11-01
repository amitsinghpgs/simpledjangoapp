from django.forms import ModelForm, Textarea
from .models import Quote

class PatialQuoteForm(ModelForm):
    class Meta:
        model=Quote
        fields = ['quote']
        help_texts = {
            'quote': ('Enter yor quote and submit'),
        }