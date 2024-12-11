from venv import logger
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, GenericAPIView, UpdateAPIView
from .models import User
from Apps.Trading.models import Wallet
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializer import (
    EmailSerializer,
    GroupSerializer,
    PermissionSerializer,
    UserSerializer,
    UserRegisterSerializer,
    UserTokenObtainPairSerializer,

)

from rest_framework.response import Response
from django.core.mail import send_mail

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.serializers import ValidationError
from django.contrib.auth import logout as django_logout
# from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import mixins
from django.db import transaction
from Common.Bast_Get_data.GetModel import Base_GetModel
from .permission import (UserPermission, PermissionPermission, GroupPermission)


class UserRegisterCreateAPIview(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self,request, *args, **kwargs ):
        # Wallet_Accout = self.request.data.get("Wallet_Accout")
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                instance = serializer.instance

                # Validate and create the Gallery object
                # if Wallet_Accout:
                    # currency = Wallet_Accout.get("BTC")
                    # balance = Wallet_Accout.get("balance")
                    # reserved = Wallet_Accout.get("reserved")
                    # admin_wallet = Wallet_Accout.get("admin_wallet")
                    
                Wallet.objects.create(
                            currency="USDT",
                            balance=0,
                            reserved=0,
                            admin_wallet=False,
                            user_id = instance
                        )
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewsets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    # def list(self, request, *args, **kwargs):
    #     # Retrieve all users
    #     users = self.queryset.all()
    #     serialized_users = []

    #     for user in users:
    #         # Create a dictionary with user data
    #         wallet_data = WalletSerializer(user.wallet_id).data if user.wallet_id else None
    #         user_data = {
    #             "id": user.id,
    #             "last_login": user.last_login,  # Last login timestamp
    #             "is_superuser": user.is_superuser,  # Superuser flag
    #             "is_staff": user.is_staff,  # Staff status
    #             "is_active": user.is_active,  # Active status
    #             "date_joined": user.date_joined,  # Account creation timestamp
    #             "is_deleted": user.is_deleted,  # Custom field for soft delete
    #             "deleted_at": user.deleted_at,  # Timestamp for soft delete
    #             "username": user.username,  # Username
    #             "email": user.email,  # Email address
    #             "password": user.password,  # Password (hashed)
    #             "created_at": user.created_at,  # Creation timestamp
    #             "updated_at": user.updated_at,  # Last update timestamp
    #             "avatar": user.avatar.url if user.avatar else None,  # Avatar URL
    #             "groups": [group.name for group in user.groups.all()],  # User groups
    #             "user_permissions": [perm.codename for perm in user.user_permissions.all()],  # User permissions
    #             "wallet_id": wallet_data,  # Nested Wallet data (if available)
    #         }
    #         serialized_users.append(user_data)

    #     return Response({"users": serialized_users}, status=status.HTTP_200_OK)
    
    # def retrieve(self, request, *args, **kwargs):

    #     try:
    #         user = self.queryset.get(pk=kwargs['pk'])
    #     except User.DoesNotExist:
    #         return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    #     wallet_data = WalletSerializer(user.wallet_id).data if user.wallet_id else None
    #     user_data = {
    #         "id": user.id,
    #         "last_login": user.last_login,  # Last login timestamp
    #         "is_superuser": user.is_superuser,  # Superuser flag
    #         "is_staff": user.is_staff,  # Staff status
    #         "is_active": user.is_active,  # Active status
    #         "date_joined": user.date_joined,  # Account creation timestamp
    #         "is_deleted": user.is_deleted,  # Custom field for soft delete
    #         "deleted_at": user.deleted_at,  # Timestamp for soft delete
    #         "username": user.username,  # Username
    #         "email": user.email,  # Email address
    #         "password": user.password,  # Password (hashed)
    #         "created_at": user.created_at,  # Creation timestamp
    #         "updated_at": user.updated_at,  # Last update timestamp
    #         "avatar": user.avatar.url if user.avatar else None,  # Avatar URL
    #         "groups": [group.name for group in user.groups.all()],  # User groups
    #         "user_permissions": [perm.codename for perm in user.user_permissions.all()],  # User permissions
    #         "wallet_id": wallet_data,  # Nested Wallet data (if available)
    #     }

    #     return Response({"user": user_data}, status=status.HTTP_200_OK)


# class UserDetailViews(Base_GetModel):
#     queryset = User.objects.all()
#     serializer_class = GetUserSerializer
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         if 'id' in kwargs:  # หากมีการส่ง ID มาใน URL จะทำการดึงข้อมูลผู้ใช้งานคนเดียว
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)  # หากไม่มี ID จะดึงรายการผู้ใช้ทั้งหมด


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [PermissionPermission]


class User_Me(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

   
class VerifyEmailAPIView(APIView):
    
    permission_classes = [ AllowAny]
    def get(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        if uid is None or token is None:
            return Response({'error': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verify = True
            user.save()
            return Response({'detail': 'Email successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        

class ResendVerificationEmailAPIView(APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            if user.is_verify == True:
                return Response({'message': 'Email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                subject = 'Verify Your Email Address'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                verify_url = f"http://localhost:8000{reverse('api:verify-email')}?uid={uid}&token={token}"

                context = {
                    'user': user,
                    'verify_url': verify_url,
                }
                convert_to_html_content =  render_to_string(
                template_name="verification_email.html",
                context = context
                )
                
                plain_message = strip_tags(convert_to_html_content)
                a = send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],   # recipient_list is self explainatory
                html_message=convert_to_html_content,
                fail_silently=True,   # Optional
                ) 
                return Response({'message': 'Verification email resent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f'Error sending email: {e}')
                print(f'Error sending email: {e}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#or TokenObtainPairView
class UserLoginView(TokenObtainPairView):
    
    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            response = super().post(request, *args, **kwargs)
            response.data.update({
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "is_verify": user.is_verify,
            })
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

