from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.SelectDateWidget(years=range(1950, 2010))
    )


    phone_number = forms.CharField(
        max_length=10,
        label="Phone Number",
    )

    # Add the "OTP" field
    otp = forms.CharField(
        max_length=6,
        label="OTP (One-Time Password)",
        help_text="Enter the 6-digit OTP sent to your phone number."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'phone_number', 'otp']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        if age < 18:
            raise ValidationError("You must be at least 18 years old to register.")

        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not (6000000000 <= int(phone_number) <= 9999999999):
            raise ValidationError("Phone number must be between 6,000,000,000 and 9,999,999,999")

        return phone_number


class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']