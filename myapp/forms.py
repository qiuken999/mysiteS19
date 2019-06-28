from django import forms
from myapp.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']

        widgets = {
            'client': forms.RadioSelect
        }

        labels = {
            "num_units": "Quantity",
            "client": "Client Name"
        }

class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=((1, 'yes'), (0, 'no')))
    quantity = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)