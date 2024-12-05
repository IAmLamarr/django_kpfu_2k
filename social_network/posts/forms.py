from django import forms
from posts.models import Keyword, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('id',)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "row": 3,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "row": 3,
                }
            ),
        }

class KeywordForm(forms.Form):
    pass