from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not (value.isdigit() and len(value) == 11):
        raise ValidationError('Customer phone number must be exactly 11 digits.')