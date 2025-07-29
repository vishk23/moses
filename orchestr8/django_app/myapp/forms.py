from django import forms
from django.core.exceptions import ValidationError

class OnDemandForm(forms.Form):
    # Define the required email domain as a class variable
    REQUIRED_EMAIL_DOMAIN = '@bcsbmail.com'
    
    email = forms.EmailField()
    key = forms.IntegerField()
    additions = forms.CharField(required=False)
    deletes = forms.CharField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith(self.REQUIRED_EMAIL_DOMAIN):
            raise ValidationError(f'Email must end with {self.REQUIRED_EMAIL_DOMAIN}')
        return email

    def clean_key(self):
        key = self.cleaned_data['key']
        if len(str(key)) > 12:
            raise ValidationError('Key must have up to 12 digits')
        return key

    def clean_additions(self):
        data = self.cleaned_data['additions']
        if data:
            try:
                # Convert comma-separated string to list of integers, stripping whitespace
                additions = [int(x.strip()) for x in data.split(',')]
                # Check each number's digit length
                for num in additions:
                    if len(str(num)) > 20:
                        raise ValidationError(f'Addition {num} has more than 20 digits')
                return additions
            except ValueError:
                raise ValidationError("Additions must be comma-separated integers.")
        return []

    def clean_deletes(self):
        data = self.cleaned_data['deletes']
        if data:
            try:
                # Convert comma-separated string to list of integers, stripping whitespace
                deletes = [int(x.strip()) for x in data.split(',')]
                # Check each number's digit length
                for num in deletes:
                    if len(str(num)) > 20:
                        raise ValidationError(f'Delete {num} has more than 20 digits')
                return deletes
            except ValueError:
                raise ValidationError("Deletes must be comma-separated integers.")
        return []