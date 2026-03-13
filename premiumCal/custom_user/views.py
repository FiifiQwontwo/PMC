from time import timezone

from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdminInvite
from .serializer import LoginSerializer, AdminUserRegistrationSerializer, AdminInviteSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class CsrfExemptAPIView(APIView):
    authentication_classes = []


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                    },
                ),
            ),
            400: 'Bad Request',
            401: 'Unauthorized',
            500: 'Internal Server Error',
        }
    )
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "success": True,
                "message": "Login successful.",
                "data": data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="User logout",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                    },
                ),
            ),
            401: 'Unauthorized',
            500: 'Internal Server Error',
        }
    )
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class AdminRegistrationView(CsrfExemptAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create an Admin User",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['full_name', 'email', 'phone', 'password', 'password2'],
            properties={
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: 'Created',
            400: 'Bad Request',
            500: 'Internal Server Error',
        }
    )
    def post(self, request):
        serializer = AdminUserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            subject = "Welcome to Premium Calculation Africa Admin Portal"
            message = f"""
Hello,

Your admin account has been created successfully.
Email: {user.email}

You can now log in to the admin portal.

Regards,
Bluespace Africa Team
""".strip()

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({
                "success": True,
                "message": "Admin account created successfully.",
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                    },
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SendAdminInviteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Send admin invite email",
        request_body=AdminInviteSerializer,
        responses={201: 'Invite sent', 400: 'Bad request'}
    )
    def post(self, request):
        serializer = AdminInviteSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            invite = serializer.save()

            invite_link = f"{request.scheme}://{request.get_host()}/admin/register/{invite.token}/"

            message = f"""
You have been invited to become an admin.

Click the link below to register:

{invite_link}

This invitation expires in 48 hours.
""".strip()

            send_mail(
                "Admin Invitation",
                message,
                settings.DEFAULT_FROM_EMAIL,
                [invite.email],
                fail_silently=False
            )

            return Response({
                "success": True,
                "message": "Admin invitation sent."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegisterWithInviteView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            invite = AdminInvite.objects.get(token=token)
        except AdminInvite.DoesNotExist:
            return Response({"error": "Invalid invite"}, status=404)

        if invite.is_used:
            return Response({"error": "Invite already used"}, status=400)

        if invite.expires_at < timezone.now():
            return Response({"error": "Invite expired"}, status=400)


        if request.data.get("email") != invite.email:
            return Response({
                "error": "This invite is only valid for the invited email."
            }, status=400)


        if CustomUser.objects.filter(email=invite.email).exists():
            return Response({
                "error": "Admin account already exists."
            }, status=400)

        serializer = AdminUserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Mark invite as used
            invite.is_used = True
            invite.save(update_fields=["is_used"])

            return Response({
                "success": True,
                "message": "Admin account created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)
