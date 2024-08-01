from django import forms
from .models import Comment, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment', ]


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['username', 'phone', 'quantity', ]

    def clean_quantity(self):
        quantity = self.data.get('quantity')
        if int(quantity) <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity

