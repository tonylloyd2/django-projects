from django import forms
from django.contrib.auth import get_user_model,authenticate

UserModel = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(LoginForm,self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = UserModel.objects.get(email=email)
            user=authenticate(
                username = email,
                password = password
            )
            if not user:
                self._errors['password'] = self.error_class(['wrong password'])
        except UserModel.DoesNotExist:
            self._errors['email'] = self.error_class(['user does not exist'])

        return self.cleaned_data

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    phone_number = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(RegisterForm,self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        try:
            user = UserModel.objects.get(email=email)
            self._errors['email'] = self.error_class(['email already in use'])
        except UserModel.DoesNotExist:
            if len(password) < 8:
                    self._errors['password'] = self.error_class(['Passswords should have 8 characters or more'])

            elif len(password) >= 8:
                if password == confirm_password:
                        user = UserModel()
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name
                        user.phone_number = "254"+phone_number[-9:]
                        user.set_password(password)
                        user.save()
                elif password != confirm_password:
                    self._errors['confirm_password'] = self.error_class(['Passswords should match'])

class ChangePasswordForm(forms.Form):
    current_passsword = forms.CharField(max_length=15)
    new_passsword = forms.CharField(max_length=15)
    confirm_passsword = forms.CharField(max_length=15)

    def clean(self):
        return self.cleaned_data

