from rest_framework.decorators import api_view
from django.shortcuts import render
from api.models import Employee


@api_view(['GET'])
def get_team_member(request):
    employee = Employee.objects.get(msysemail=request.user)
    team_members= Employee.objects.filter(reporting_to=employee.emp_id,is_active=1)
    return render(request,'teammembers.html', {'data': request.user,'teammembers': team_members})



