from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .serializers import EmployeeSerializer
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.core import serializers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import Employee

import datetime


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
        data = request.data
        try:
            validate_email(data['email'])
        except:
            return JsonResponse({'error':f'email not valid'})
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = Employee.objects.create(
                name=data['name'],
                email=data['email'],
                department=data['department'],
                salary=data['salary'],
                birth_date = data['birth_date']
            )
            return JsonResponse(serializer.data, safe=False,status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse({"error": serializer.errors},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET','PUT','DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def employee_details(request, employee_id):

    if request.method == 'GET':

        employee = list(Employee.objects.filter(id=employee_id).values())
        return JsonResponse(employee[0], safe=False,status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data
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
    recent_date = Employee.objects.all().aggregate(Max('birth_date'))
    max_employee = list(Employee.objects.filter(birth_date=recent_date['birth_date__max']).values())[0]
    older_date = Employee.objects.all().aggregate(Min('birth_date'))
    min_employee = list(Employee.objects.filter(birth_date=older_date['birth_date__min']).values())[0]
    today = datetime.datetime.today()
    youngest_age = today.year - recent_date['birth_date__max'].year
    olderst_age = today.year - older_date['birth_date__min'].year
    average = float(youngest_age + olderst_age)/2
    content = {"younger": max_employee, "older": min_employee, "average": average}
    return JsonResponse(content,status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def err_404(request, exception=None):
    content = {"error":"this route doesnt exists"}
    return JsonResponse(content,status=status.HTTP_404_NOT_FOUND)