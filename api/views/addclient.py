import json
from django.shortcuts import render
from api.models import ClientDetails,Employee,ProjectDetails


def add_client(request):
    employee = Employee.objects.get(msysemail=request.user)
    newclient = ClientDetails()
    newproject = ProjectDetails()
    client_list = ClientDetails.objects.all()
    project_list = ProjectDetails.objects.all()
    if request.method == 'POST':
        newclient.client_code = 'CLI-' + str(ClientDetails.objects.count() + 1).zfill(3)
        newproject.project_code = 'PRO-' + str(ProjectDetails.objects.count() + 1).zfill(3)
        newclient.emp_id=employee
        newclient.client_name = request.POST.get('cli_name')
        newclient.client_location = request.POST.get('cli_location')
        newproject.projectname = request.POST.get('project_name')
        newproject.pm_emp_id = request.POST.get('project_manager')
        newproject.client_code_id = newclient.client_code
        newclient.save()
        newproject.save()

    return render(request, 'addingclient.html', {'status': 'success', 'client_list':client_list,'project_list':project_list})

