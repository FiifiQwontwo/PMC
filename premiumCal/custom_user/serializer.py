from rest_framework import serializers
from .models import CustomUser, AdminInvite
from .models import Staff, Admin
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class StaffUserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True)
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser.objects.create(
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            is_active=True,
            is_staff=True
        )

        user.set_password(validated_data['password'])
        user.save()

        Staff.objects.create(
            user=user,
            full_name=validated_data['full_name']
        )

        return user


class AdminUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True)
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'full_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser.objects.create(
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(validated_data['password'])
        user.save()

        Admin.objects.create(
            user=user,
            full_name=validated_data['full_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError("Invalid email or password.")

            if not user.is_active:
                raise serializers.ValidationError("Account is not active.")

        else:
            raise serializers.ValidationError("Email and password are required.")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']

        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class AdminInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminInvite
        fields = ['email']

    def create(self, validated_data):
        request = self.context['request']

        invite = AdminInvite.objects.create(
            email=validated_data['email'],
            invited_by=request.user
        )

        return invite


