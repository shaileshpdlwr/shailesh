from django import forms
from .models import Comment

class EmailForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']




