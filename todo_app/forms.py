from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model
from django import forms
from .models import Category, ToDo

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super.__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class ToDoForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label='カテゴリー',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = ToDo
        fields = ('title', 'category')


"""
    category = forms.ModelMultipleChoiceField(
        label="カテゴリー",
        queryset=Category.objects.all(),
        widget=forms.Select,)
"""