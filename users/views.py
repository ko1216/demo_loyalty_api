import string
import random
from datetime import timedelta, datetime, timezone

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, SMSCode, Invitation
from users.tasks import send_sms
from users.serializares import UserRegistrationSerializer, UserSerializer
from users.services import generate_invite_code


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        request.session['phone_number'] = phone_number

        user = User.objects.filter(phone_number=phone_number)
        if not user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            user.invite_code = generate_invite_code()
            user.save()
        else:
            user = User.objects.get(phone_number=phone_number)

        code = ''.join(random.choices(string.digits, k=4))
        sms_code = SMSCode.objects.create(user=user, code=code)

        send_sms(sms_code.code, user.phone_number)

        return Response({'message': 'SMS code sent successfully'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        phone_number = request.session.get('phone_number')
        if not phone_number:
            return Response({'error': 'phone number not found in session'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number not found'}, status=status.HTTP_404_NOT_FOUND)

        sms_code = SMSCode.objects.filter(user=user, code=code).order_by('-created_at').first()
        if not sms_code:
            return Response({'error': 'SMS code not found'}, status=status.HTTP_400_BAD_REQUEST)

        expiration_time = sms_code.created_at + timedelta(minutes=5)
        if expiration_time > datetime.now(timezone.utc):
            sms_code.delete()
        else:
            return Response({'error': 'Verification code has expired'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user)

        response_data = {
            'access': str(token.access_token),
            'refresh': str(token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InvitationActivate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite_code = request.data.get('invite_code')

        owner = User.objects.filter(invite_code=invite_code).first()
        if not owner:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user

        if Invitation.objects.filter(activated_by=user).exists():
            return Response({'error': 'This or another invite code already activated by the current user'},
                            status=status.HTTP_400_BAD_REQUEST)

        invitation, created = Invitation.objects.get_or_create(code=invite_code)
        if created:
            invitation.user = owner
            invitation.save()
            invitation.activated_by.add(user)
        else:
            invitation.activated_by.add(user)

        return Response({'message': 'Invite code activated successfully'}, status=status.HTTP_201_CREATED)
