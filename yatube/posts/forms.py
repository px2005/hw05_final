from django import forms
from django.forms import ModelForm, Textarea, Select

from .models import Post, Comment


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'А кто поле будет заполнять?',
            params={'value': value},
        )


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст'
            }),
            'group': Select(attrs={
                'class': 'form-control',
            })
        }

        def validate_not_empty(self):
            data = self.cleaned_data['text']
            if data == '':
                raise forms.ValidationError(
                    'А кто поле будет заполнять?',
                    params={'data': data},
                )
            return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Комментарий'
        }
        help_texts = {
            'text': 'текст комментария.'
        }
