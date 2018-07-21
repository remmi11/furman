from django import forms

#from .models import Form
from .models import Form, Form500, MasterGeom

# class PostForm(forms.ModelForm):

#     class Meta:
#         model = Form
#         fields = ('__all__')


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Form500
        fields = ('__all__')

class newForm(forms.ModelForm):
    
    class Meta:
        model = MasterGeom
        fields = ('__all__')