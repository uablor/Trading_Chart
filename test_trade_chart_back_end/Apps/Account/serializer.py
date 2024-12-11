from rest_framework.serializers import ModelSerializer
from .models import (User)
from Apps.Trading.models import Wallet
from django.contrib.auth.models import (Group, Permission)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ["email", "password", "password2","username"] ##  "first_name", "last_name", "phone"
        
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        validated_data['is_verify'] = False
        validated_data["is_active"] = True
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(ModelSerializer):
    
    class Meta:
        fields = "__all__"
        model = User
        extra_kwargs = {
            "last_login": {"required": False},
            "date_joined": {"required": False},
            "created_at": {"required": False},
            "updated_at": {"required": False},
            "updated_at": {"required": False},
            "password": {"write_only": True},
        }

    def validate_password(self, value):

        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        validated_data['is_verify'] = False
        validated_data["is_active"] = True

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if self.instance:
            fields.pop("password")

        if request.method in ["POST", "PUT", "PATCH"]:
            user = request.user
            if (
                not user.is_superuser
                and not user.groups.filter(permissions__codename=" ").exists()
                ):
                fields.pop("is_staff")
                fields.pop("is_superuser")
                fields.pop("groups")
                fields.pop("user_permissions")
        return fields
        
        
class GroupSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group
   
        
class PermissionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Permission
        

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    class Meta:
        fields = "email"
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is not associated with any account.")
        return value


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["is_verify"] =  user.is_verify

        return token

    def validate(self, attrs):
        # ตรวจสอบผู้ใช้จาก email
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('อีเมลนี้ไม่ได้ลงทะเบียน.')

        # ตรวจสอบการยืนยันตัวตนโดยใช้ email และรหัสผ่าน
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('รหัสผ่านไม่ถูกต้อง.')
        
        # ตรวจสอบการยืนยันบัญชีผู้ใช้
        if not user.is_verify:
            raise AuthenticationFailed('บัญชีผู้ใช้ยังไม่ได้รับการยืนยัน กรุณายืนยันอีเมลของคุณ.')

        # ส่งคืนข้อมูลที่ได้รับการตรวจสอบพร้อม JWT token
        return super().validate(attrs)