from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Employee

def employee_detail(request, id):
   employee_details = get_object_or_404(Employee, pk=id)
   context = {
    "employee": employee_details
   }
   return render(request, "employee_detail.html", context=context)