from django import forms
from .models import Comment


"""
 The comment form
"""


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
