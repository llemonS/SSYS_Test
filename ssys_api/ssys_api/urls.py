from django.conf.urls import handler404, handler500, handler403, handler400
from django.contrib import admin
from django.urls import path, include

from employees import views

handler404 = views.err_404

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('registration/', include('rest_auth.registration.urls'), name='registration'),
    path('employees', views.employees, name='employees'),
    path('employees/<int:employee_id>', views.employee_details, name='employee_details'),
    path('reports/employees/salary/', views.salary_reports, name="salary_reports"),
    path('reports/employees/age/', views.age_reports, name="age_reports")
]

