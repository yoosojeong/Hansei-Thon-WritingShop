from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from taggit.forms import *
from .models import *

class WritePostForm(forms.ModelForm):

    content = forms.CharField(required=True)
    tags = TagField()

    def __init__(self, user, *args, **kwargs):        
        super(WritePostForm, self).__init__(*args, **kwargs)

        self.fields['images'].required = False
        self.fields['user']=forms.ModelChoiceField(queryset=User.objects.filter(username=user))
        
        self.fields['content'].widget = forms.Textarea(attrs={
            'class': 'form-control form-control-sm mb-1',
            'name': 'title',
            'autocomplete': 'off',
            'required':'requireds',
            'placeholder': '함께 올릴 말'
            })
        
        self.fields['tags'].widget = forms.TextInput(attrs={
            'class': 'form-control form-control-sm mb-1 inl',
            'name': 'title',
            'autocomplete': 'off',
            'required':'requireds',
            'placeholder': '예) 사랑, 비, 이별,'
            })

    class Meta:
        model = WritePostModel

        fields = ('user', 'images', 'content', 'tags',)



class SearchForm(forms.ModelForm): 

    word = forms.CharField(required=True)

    class Meta:
        model = SearchData

        fields = ('word',)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['word'].widget = forms.TextInput(attrs={
            'id': 'search-input tex',
            'name': 'word',
            'autocomplete': 'off',
            'required':'requireds'})