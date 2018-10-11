from django import forms

#from .models import Form
from .models import MasterGeom, Users, FormAll

# class PostForm(forms.ModelForm):

#     class Meta:
#         model = Form
#         fields = ('__all__')


class PostForm(forms.ModelForm):

    class Meta:
        model = FormAll
        fields = ('__all__')

class newForm(forms.ModelForm):
    
    class Meta:
        model = MasterGeom
        fields = ('__all__')


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    
    class Meta:
        model = Users
        fields = ('username', 'email', 'edit_auth')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        form = super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'edit_auth')

    def __init__(self, *args, **kwargs):
        form = super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label