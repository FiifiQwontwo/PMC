from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import AdditionalCost
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import ListAdditional_costSerializer, CreateAdditional_costSerializer, UpdateAdditionalCostSerializer, \
    Additional_costDetailSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib import messages


# Create your views here.
class ListAdditionalCostView(APIView):
    template_name = 'Additional_cost/list.html'

    @swagger_auto_schema(
        operation_description="List Additional Cost Type",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'brown_card_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                description="brown_card_charge"),
                            'nic_contribution_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                      description="nic_contribution_charge"),
                            'sticker_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="sticker_charge"),
                            'age_loading_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                 description="age_loading_charge"),
                            'age_loading_percentage': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                     description="age_loading_percentage"),
                            'educational_fee': openapi.Schema(type=openapi.TYPE_NUMBER, description="educational_fee"),
                            'gia_levy': openapi.Schema(type=openapi.TYPE_NUMBER, description="gia_levy"),
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
        additional = AdditionalCost.objects.only('brown_card_charge', 'nic_contribution_charge', 'sticker_charge',
                                                 'age_loading_charge', 'age_loading_percentage', 'educational_fee',
                                                 'gia_levy')

        if not additional.exists():
            return Response({
                'success': True,
                'message': 'No additional cost Found',
                'additional': [],
                'count': 0
            }, status=status.HTTP_200_OK)
        serializer = ListAdditional_costSerializer(additional, many=True)
        if request.accepted_renderer.format == 'html':
            return Response(
                {
                    'additional': serializer.data,
                },
                template_name=self.template_name
            )

        return Response({
            'success': True,
            'additional cost': serializer.data,
            'count': additional.count()
        }, status=status.HTTP_200_OK)


class CreateAdditional_costView(APIView):
    template_name = 'Additional_cost/add.html'
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Create a new ClassType",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'brown_card_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="brown_card_charge"),
                'nic_contribution_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                          description="nic_contribution_charge"),
                'sticker_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="sticker_charge"),
                'age_loading_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="age_loading_charge"),
                'age_loading_percentage': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                         description="age_loading_percentage"),
                'educational_fee': openapi.Schema(type=openapi.TYPE_NUMBER, description="educational_fee"),
                'gia_levy': openapi.Schema(type=openapi.TYPE_NUMBER, description="gia_levy"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Id"),
                        'brown_card_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="brown_card_charge"),
                        'nic_contribution_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                  description="nic_contribution_charge"),
                        'sticker_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="sticker_charge"),
                        'age_loading_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description="age_loading_charge"),
                        'age_loading_percentage': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                 description="age_loading_percentage"),
                        'educational_fee': openapi.Schema(type=openapi.TYPE_NUMBER, description="educational_fee"),
                        'gia_levy': openapi.Schema(type=openapi.TYPE_NUMBER, description="gia_levy"),
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
            serializer = CreateAdditional_costSerializer(
                data=request.data,
                context={'request': request}
            )

            if serializer.is_valid():
                additional_cost = serializer.save()
                messages.success(request, "Additional Cost Create successfully")

                if request.accepted_renderer.format == 'html':
                    return redirect('additional_cost:list_additional_cost_endpoint')

                return Response({
                    'success': True,
                    'message': 'Additional cost created successfully.',
                    'data': additional_cost.data
                }, status=status.HTTP_201_CREATED)

            if request.accepted_renderer.format == 'html':
                return render(
                    request,
                    self.template_name,
                    {'errors': serializer.errors, 'old_data': request.data}
                )

            return Response({
                'success': False,
                'message': 'Failed to create Additional cost.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Unexpected error during Additional Cost creation.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error loading creation form.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Additional_CostDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve Additional Cost details by ID",
        responses={
            200: 'OK',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def get(self, request, pk):
        try:
            additional = get_object_or_404(AdditionalCost, pk=pk)
            serializer = Additional_costDetailSerializer(AdditionalCost)

            if request.accepted_renderer.format == 'html':
                messages.success(request,
                                 f"Additional_Cost'{AdditionalCost.sticker_charge}' details retrieved successfully.")
                return render(request, 'Additional_cost/detail.html', {'additional': serializer.data})

            return Response({
                'success': True,
                'message': 'Additional_Cost details retrieved successfully.',
                'additional': serializer.data
            }, status=status.HTTP_200_OK)

        except AdditionalCost.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Additional_Cost not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error retrieving Additional_Cost details.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateAdditional_CostView(APIView):
    template_name = 'Additional_cost/update.html'
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Update an existing Additional Cost",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'brown_card_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="brown_card_charge"),
                'nic_contribution_charge': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                          description="nic_contribution_charge"),
                'sticker_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="sticker_charge"),
                'age_loading_charge': openapi.Schema(type=openapi.TYPE_NUMBER, description="age_loading_charge"),
                'age_loading_percentage': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                         description="age_loading_percentage"),
                'educational_fee': openapi.Schema(type=openapi.TYPE_NUMBER, description="educational_fee"),
                'gia_levy': openapi.Schema(type=openapi.TYPE_NUMBER, description="gia_levy"),
            }
        ),
        responses={
            200: 'OK',
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def put(self, request, **kwargs):
        try:
            additional_cost_id = kwargs.get('pk')
            model = get_object_or_404(AdditionalCost, pk=additional_cost_id)
            serializer = UpdateAdditionalCostSerializer(model, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Additional Cost updated successfully.")

                if request.accepted_renderer.format == 'html':
                    return redirect('additional_cost:list_additional_cost_endpoint')

                if request.accepted_renderer.format == 'html':
                    return render(
                        request,
                        self.template_name,
                        {'additional_cost': serializer.data, 'message': "Additional Cost updated successfully."},
                        status=200
                    )

                return Response({
                    'success': True,
                    'message': 'Additional Cost updated successfully.',
                    'cargo_type': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'success': False,
                'message': 'Failed to update Additional Cost.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'Unexpected error during update.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Delete_Additional_CostView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Delete a Additional Cost by ID",
        responses={
            200: 'Additional Cost deleted successfully.',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def delete(self, request, pk):
        try:
            additional_cost = AdditionalCost.objects.get(pk=pk)
            additional_cost.delete()
            messages.success(request, "Additional Cost deleted successfully.")

            if request.accepted_renderer.format == 'html':
                return redirect('list_additional_cost_endpoint')

            return Response({
                'success': True,
                'message': 'Additional Cost deleted successfully.'
            }, status=status.HTTP_200_OK)

        except AdditionalCost.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Additional Cost not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error occurred while deleting Additional Cost',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
