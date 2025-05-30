from rest_framework.decorators import api_view
from django.shortcuts import render
from api.models import Employee

@api_view(['GET'])
def get_profile(request):
    employee = Employee.objects.get(msysemail=request.user)
    return render(request,'profile.html', {'data': request.user,'profile': employee})

