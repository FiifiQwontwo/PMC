from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Currency_Rate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import List_Currency_Rate_Serializer, Create_Currency_RateSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib import messages


class ListCurrency_RateView(APIView):
    template_name = 'currency/list.html'

    @swagger_auto_schema(
        operation_description="List Currency Rate",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'currency_name': openapi.Schema(type=openapi.TYPE_STRING, description="currency Name"),
                            'currency_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description="currency rate"),
                            'currency_shortrate_charge': openapi.Schema(type=openapi.TYPE_STRING,
                                                                        description="Currency Short Rate Charge"),
                            'currency_symbol': openapi.Schema(type=openapi.TYPE_STRING, description="currency Symbol"),
                        },
                    ),
                ),
            ),
            400: openapi.Response(description="Bad Request"),
            401: openapi.Response(description="Unauthorized"),
            403: openapi.Response(description="Forbidden"),
            500: openapi.Response(description="Internal Server Error"),
        }
    )
    def get(self, request):
        currency = Currency_Rate.objects.only('currency_name', 'currency_rate', 'currency_shortrate_charge',
                                              'currency_symbol')

        if not currency.exists():
            return Response({
                'success': True,
                'message': 'No Currency Found',
                'currency': [],
                'count': 0
            }, status=status.HTTP_200_OK)

        serializer = List_Currency_Rate_Serializer(currency, many=True)
        if request.accepted_renderer.format == 'html':
            return Response(
                {'currency': serializer.data,
                 },
                template_name=self.template_name
            )

        return Response({
            'success': True,
            'currency': serializer.data,
            'count': currency.count()
        }, status=status.HTTP_200_OK)


class CreateCurrency_RateView(APIView):
    template_name = 'currency/create.html'
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Create a new Currency",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'currency_name': openapi.Schema(type=openapi.TYPE_STRING, description="currency Name"),
                'currency_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description="currency rate"),
                'currency_shortrate_charge': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description="Currency Short Rate Charge"),
                'currency_symbol': openapi.Schema(type=openapi.TYPE_STRING, description="currency Symbol"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Id"),
                        'currency_name': openapi.Schema(type=openapi.TYPE_STRING, description="currency Name"),
                        'currency_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description="currency rate"),
                        'currency_shortrate_charge': openapi.Schema(type=openapi.TYPE_STRING,
                                                                    description="Currency Short Rate Charge"),
                        'currency_symbol': openapi.Schema(type=openapi.TYPE_STRING, description="currency Symbol"),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                     description="Created At"),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                     description="Updated At"),
                    },
                ),
            ),
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            500: 'Internal Server Error',
        }
    )
    def post(self, request):
        try:
            serializer = Create_Currency_RateSerializer(data=request.data,
                                                        context={'request': request}
                                                        )
            if serializer.is_valid():
                currency = serializer.save(created_by=request.user)

                messages.success(request, 'Currency Rate created successfully.')
                if request.accepted_renderer.format == 'html':
                    return redirect('currency:list')

                response_serializer = Create_Currency_RateSerializer(currency)

                return Response({
                    'success': True,
                    'message': 'Currency Rate created successfully.',
                    'data': serializer.data
               }, status=status.HTTP_201_CREATED)

            if request.accepted_renderer.format == 'html':
                return render(
                    request,
                    self.template_name,
                    {'errors': serializer.errors, 'data': request.data}
                )
            return Response({
                'success': False,
                'message': 'Failed to create Currency Rate',
                'errors': serializer.errors
            },  status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'An error occurred while creating the Currency Rate',
               'errors': str(e)
           }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
