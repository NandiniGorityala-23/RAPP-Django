from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from api.models import ProjectDetails,ClientDetails,Employee
from lib.client_response import ClientResponse
from api.serializer.projects_serializer import ProjectDetailsSerializer,ClientDetailsSerializer

res_obj = ClientResponse()

def get_object(request,code):
    """This is for getting particular project object"""
    employee = Employee.objects.get(msysemail=request.user)
    try:
        return ProjectDetails.objects.filter(client_code_id=code)
    except ProjectDetails.DoesNotExist:
        return False

@login_required(login_url='/login/')
@api_view(['GET'])
def get_projects(request, client_code):

    """To get all projects based on particular client"""

    project = get_object(request,client_code)
    if project:
        projectserializer = ProjectDetailsSerializer(project, many=True)
        project_list = []
        for proj in projectserializer.data:
            project_dic = {}
            project_dic['code']=proj.get('project_code')
            project_dic['name']=proj.get('projectname')
            project_list.append(project_dic)
        response = res_obj.response_formation(project_list)
        return Response(response)
    else:
        response = res_obj.response_formation({})
        return Response(response)

@ensure_csrf_cookie
@api_view(['GET'])
def get_client(request):

    """To get client details"""

    client = ClientDetails.objects.all()
    serializer = ClientDetailsSerializer(client, many=True)
    client_list = []
    for cli in serializer.data:
            cli_dic = {}
            cli_dic['code']=cli.get('client_code')
            cli_dic['name']=cli.get('client_name')
            client_list.append(cli_dic)
    response = res_obj.response_formation(client_list)
    return Response(response)

