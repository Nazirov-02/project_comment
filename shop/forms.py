from django import forms
from phonenumber_field.formfields import PhoneNumberField


class OrderForm(forms.Form):
    name = forms.CharField()
    phone_number = PhoneNumberField(region="UZ")
    quantity = forms.IntegerField()

class CommentForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)