from django import forms
from .models import Product
from .models import Comments1
from .models import Comments2
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'year',
            'city',
            'nominal',
            'bank',
            'nb',
            'metall',
            'price',
        )
        widgets = {
            'title': forms.TextInput,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments1
        fields = (
            'dated',
            'name',
            'url_lot',
            'url_saler',
            'current_price',
            'my_current_price',
            'status',
            'stack',
            'post_price',
            'name_saler',
            'comment_id',
            'buy',
            # 'colored_name',
        )
        widgets = {
            'title': forms.TextInput,
        }

class CommentForm2(forms.ModelForm):
    class Meta:
        model = Comments2
        fields = (
            'dated',
            'name',
            'url_lot',
            'url_saler',
            'current_price',
            'my_current_price',
            'status',
            'stack',
            'post_price',
            'name_saler',
            'comment_id',
            'buy',
            # 'colored_name',
        )
        widgets = {
            'title': forms.TextInput,
        }