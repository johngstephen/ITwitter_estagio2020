from django import forms


class CreateAccountForm(forms.Form):
    user_first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-group'}))
    user_last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-group'}))
    username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-group'}))
    user_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-group'}))
    user_password_confirm = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-group',
            'placeholder': 'Confirm Password'
        }
    ))
    user_email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'E-mail Address', 'class': 'form-group'}))

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        password = cleaned_data.get("user_password")
        confirm_password = cleaned_data.get("user_password_confirm")

        if password != confirm_password:
            raise forms.ValidationError(
                "Both password fields must be equal!"
            )
