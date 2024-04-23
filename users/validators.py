from rest_framework import serializers


class PhoneNumberValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not value:
            raise serializers.ValidationError(
                {
                    'detail':
                        'Field "phone" is required'
                }
            )
