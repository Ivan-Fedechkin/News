from django import forms
from .models import Post, Category
from .models import Author

class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        label='Автор',
        queryset=Author.objects.order_by('-user').all(),
        empty_label='Выберите автора',
    )
    heading_post = forms.CharField(
        label='Название - заголовок'
    )
    text_post = forms.CharField(label='Текст', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = [
            'heading_post',
            'text_post',
            'category',
            'author',
            'select_choices'
        ]
