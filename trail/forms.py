# Imports #
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    The comment form
    """
    class Meta:
        model = Comment
        fields = ('body',)
