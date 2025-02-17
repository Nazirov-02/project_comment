from django import forms
from phonenumber_field.formfields import PhoneNumberField

from shop.models import Product, Comment,Order



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'quantity']

class CommentForm(forms.ModelForm):
     class Meta:
        model = Comment
        fields = '__all__'

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='__all__'
