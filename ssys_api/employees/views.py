from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import EmployeeSerializer
from django.http import JsonResponse
from rest_framework import status
from .models import Employee

# Create your views here.
#TODO:
#employees list GET
#employees create POST
#employees/ID UPDATE
#employees/ID DELETE
#employees/ID GET
#reports/employees/salary/ highest, lowest average fields GET
#reports/employees/age/ highest, lowest average fields GET


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def home(request):
    content = {"message":"bem vindo a API da SSYS"}
    return JsonResponse(content, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def employees(request):
    if request.method == 'GET':
        content = {"message":"bem vindo a API da SSYS"}
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        try:
            employee = Employee.objects.create(
                name=data['name'],
                email=data['email'],
                department=data['department'],
                salary=data['salary'],
                birth_date = data['birth_date']
            )
            serializer = EmployeeSerializer(employee)
            return JsonResponse({'employee': serializer.data}, safe=False,status=status.HTTP_201_CREATED)
        except Exception:
                return JsonResponse({'error':'something went wrong'},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)