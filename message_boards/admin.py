from django import forms
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Advertsement

class AdvertsementAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Advertsement
        fields = '__all__'


@admin.register(Advertsement)
class AdvertsementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'category')
    form = AdvertsementAdminForm
