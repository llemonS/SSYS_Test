from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Max, Min
from rest_framework.parsers import JSONParser 
from .serializers import EmployeeSerializer
from django.http import JsonResponse
from rest_framework import status
from django.core import serializers
from .models import Employee
import json

# Create your views here.
#TODO:
#employees list GET, done
#employees create POST, done
#employees/ID UPDATE, done
#employees/ID DELETE, done
#employees/ID GET, done
#reports/employees/salary/ highest, lowest average fields GET, done
#reports/employees/age/ highest, lowest average fields GET

#validator email field

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
        content = Employee.objects.all()
        serializer = EmployeeSerializer(content, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            employee = Employee.objects.create(
                name=data['name'],
                email=data['email'],
                department=data['department'],
                salary=data['salary'],
                birth_date = data['birth_date']
            )
            serializer = EmployeeSerializer(employee, many=True)
            return JsonResponse(serializer.data, safe=False,status=status.HTTP_201_CREATED)
        except Exception as e:
                return JsonResponse({'error':f'something went wrong {e}'},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(['GET','PUT','DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def employee_details(request, employee_id):

    if request.method == 'GET':

        employee = list(Employee.objects.filter(id=employee_id).values())
        return JsonResponse(employee[0], safe=False,status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return JsonResponse({'error':f'something went wrong {e}'},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        try:
            employee = Employee.objects.filter(id=employee_id)
            employee.delete()
            content = {"message":"employee deleted with success"}
            return JsonResponse(content,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error':f'something went wrong {e}'},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def salary_reports(request):
    max_salary = Employee.objects.all().aggregate(Max('salary'))
    max_employee = list(Employee.objects.filter(salary=max_salary['salary__max']).values())[0]
    min_salary = Employee.objects.all().aggregate(Min('salary'))
    min_employee = list(Employee.objects.filter(salary=min_salary['salary__min']).values())[0]
    average_salary = Employee.objects.all().aggregate(Avg('salary'))
    content = {"lowest": min_employee, "highest": max_employee, "average":average_salary["salary__avg"]}
    return JsonResponse(content,status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def age_reports(request):
    max_age = Employee.objects.all().aggregate(Max('birth_date'))
    max_employee = list(Employee.objects.filter(salary=max_age['salary__max']).values())[0]
    min_age = Employee.objects.all().aggregate(Min('birth_date'))
    min_employee = list(Employee.objects.filter(salary=min_age['salary__min']).values())[0]
    average_salary = Employee.objects.all().aggregate(Avg('salary'))
    content = {"lowest": min_employee, "highest": max_employee, "average":average_salary["salary__avg"]}
    return JsonResponse(content,status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def err_404(request, exception=None):
    content = {"error":"this route doesnt exists"}
    return JsonResponse(content,status=status.HTTP_404_NOT_FOUND)