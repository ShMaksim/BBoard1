from django import forms
from .models import Post, Response, Subscription
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'image1', 'image2', 'video1', 'video2', 'category']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['newsletter']