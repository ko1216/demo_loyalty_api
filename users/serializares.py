from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers

from users.models import User, Invitation
from users.validators import PhoneNumberValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[PhoneNumberValidator('phone')])

    def validate(self, data):
        validate_international_phonenumber(data['phone_number'])
        return data

    class Meta:
        model = User
        fields = ('id', 'phone_number',)


class UserSerializer(serializers.ModelSerializer):
    invitation = serializers.SerializerMethodField()
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'invite_code', 'invitation', 'invited_users')

    def get_invitation(self, obj):
        try:
            invitation = Invitation.objects.get(activated_by=obj)
            return invitation.code
        except Invitation.DoesNotExist:
            return None

    def get_invited_users(self, obj):
        try:
            invitation = Invitation.objects.get(user=obj)
            return [str(phone_number) for phone_number in invitation.activated_by.values_list('phone_number', flat=True)]
        except Invitation.DoesNotExist:
            return []
