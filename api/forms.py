from django import forms

from api.models import UserAdmin

class RegisterForm(forms.ModelForm):
    
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=255)

    class Meta:
        model = UserAdmin
        fields = ('user_name','password',)


class reset_form(forms.Form):


    old_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Your Old Password',  'class' : 'span'}))
    newpassword = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Your New Password',  'class' : 'span'}))
    confirm= forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'}))


    def clean(self):
        if 'new_password' in self.cleaned_data and 'confirm' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['confirm']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data