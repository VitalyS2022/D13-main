from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from .models import Advertsement, Category, Replies, News


class AdvertsementForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Advertsement
        # fields = '__all__'
        fields = [
            "title",
            "body",
            "category",
        ]

class RepliesForm(forms.ModelForm):
    body = forms.Textarea()

    class Meta:
        model = Replies
        fields = ["body"]


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "body"]