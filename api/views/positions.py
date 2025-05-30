from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from django.shortcuts import render
# import ast
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage

from lib.client_response import ClientResponse, bad_request
from lib.decorators import group_required
from api.models import  ClientDetails,Qualification,Designation,RequestType,Location,\
                        JobType,JobDetails,ProjectDetails,Employee,Skillset,UserAdmin,\
                        Candidate
from api.serializer.position_serializer import SkillSerializer,EmployeeSerializer,JobSerializer
from api.serializer.user_serializer import UserSerializer
import datetime
import uuid

res_obj = ClientResponse()


def manage_position(action, request, id=None):
    """
    This is to add/update a positions
    """
    approved_by = 'RMG'
    if action == 'add':
        job = JobDetails()
        job.rec_id = 'REC-'+ str(JobDetails.objects.count()+1).zfill(3)
    elif action == 'update' and id:
        job = JobDetails.objects.get(rec_id=id)
    elif action == 'delete' and id:
        job = JobDetails.objects.get(rec_id=id)
        # checking candidate dependancy to prevent deletion of position
        candidate = Candidate.objects.filter(rec_id=id).count()
        if candidate and job.status:
            return False
        job.is_deleted=1
        job.save()
        return True

    employee = Employee.objects.get(msysemail=request.user)

    data = json.loads(request.body)

    skillset = data.get('skills')
    skillset_data = ', '.join(skillset)

    interview_details = ', '.join(data.get('interview_det'))

    no_of_positions = int(data.get('no_of_positions'))
    selected_candidate_count = Candidate.objects.filter(rec_id=id, hr_approved=1, status="SELECTED").count()
    if no_of_positions == selected_candidate_count:
        job.status = False
        approved_by = ""
        job.closed_at = datetime.datetime.now().date()
    elif no_of_positions < selected_candidate_count:
        return False
    job.no_of_positions = no_of_positions

    job.project_code_id = data.get('project_code')
    job.client_name = data.get('client_name')
    job.experience = data.get('experience')
    job.qualification = data.get('qualification')
    job.demand_type = data.get('demand_type')
    job.request_type = data.get('request_type')
    job.skill_set = skillset_data
    job.location = data.get('location')
    job.client_interview = data.get('client_interview')
    job.job_type = data.get('job_type')
    job.designation = data.get('designation')
    job.billable = data.get('billing_type')
    job.job_description = data.get('job_description')
    job.interview_details = interview_details
    job.approved_by = approved_by
    if data.get('bill_date'):
        job.bill_date = datetime.datetime.strptime(str(data.get('bill_date')), "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        job.bill_date = None
    job.pm_emp_id = employee.emp_id
    job.save()
    return True


@ensure_csrf_cookie
@api_view(['GET'])
def get_skills(request):
    """
    This is for getting skillset
    """
    skill = Skillset.objects.all()
    serializer = SkillSerializer(skill, many=True)
    skillset = []
    for sk in serializer.data:
        skillset.append(sk.get('skill_set'))
    response = res_obj.response_formation(skillset)
    return Response(response)

@ensure_csrf_cookie
@api_view(['GET'])
def get_employee(request):
    """
    This is for getting skillset
    """
    employee = Employee.objects.all()
    serializer = EmployeeSerializer(employee, many=True)
    employee_list = []
    for emp in serializer.data:
        employee_dic = {}
        employee_dic['id']=emp.get('emp_id')
        employee_dic['name']=emp.get('name')
        employee_dic['email']=emp.get('msysemail')
        employee_dic['is_active']=emp.get('is_active')
        employee_list.append(employee_dic)
    response = res_obj.response_formation(employee_list)
    return Response(response)


def get_all_position(request):
    """
    This is to register new user using django form
    """
    employee = Employee.objects.get(msysemail=request.user)     
    client_details = ClientDetails.objects.all()
    qualification = Qualification.objects.all()
    designation = Designation.objects.all()
    requesttype = RequestType.objects.all()
    location = Location.objects.all()
    job_type = JobType.objects.all()
    job_details = JobDetails.objects.filter(pm_emp_id=employee.emp_id, is_deleted=0)
    serializer = JobSerializer(job_details, many=True)
    job_list = []
    for job in serializer.data:
        candidate_count = Candidate.objects.filter(rec_id=job.get('rec_id'), hr_approved=1, status="SELECTED").count()
        job_dic = {}
        job_dic['rec_id']=job.get('rec_id')
        d = job.get('ts').split('T')
        job_dic['date']=datetime.datetime.strptime(d[0],"%Y-%m-%d").strftime("%d/%m/%Y")
        proj = ProjectDetails.objects.get(project_code=job.get('project_code'))
        client = ClientDetails.objects.get(client_code=job.get('client_name'))
        job_dic['client']=client.client_name
        job_dic['project']=proj.projectname
        job_dic['location']=job.get('location')
        job_dic['designation']=job.get('designation')
        job_dic['skills']=job.get('skill_set')
        job_dic['request_type']=job.get('request_type')
        job_dic['no_of_positions']=job.get('no_of_positions')
        job_dic['status']=job.get('status')
        job_dic['approved_by']=job.get('approved_by')
        job_dic['interview_remarks']=job.get('interview_remarks')
        job_dic['selected_candidate_count']=candidate_count
        job_list.append(job_dic)
    data = {'data':request.user,
            'clients':client_details,
            'qualification':qualification,
            'designation':designation,
            'requesttype':requesttype,
            'location':location,
            'job_type':job_type,
            'response':job_list
            }
    return data


@group_required('PM')
def position_list(request):
    if request.method == 'POST':
        manage_position('add', request)
        return render(request,'position.html',{'status':'success'})
    elif request.method == 'GET':
        data = get_all_position(request)
        return render(request, 'position.html', data)


@group_required('PM')
def position_detail(request, id):
    if request.method == 'GET':
        print('GET one')
    elif request.method == 'PUT':
        res = manage_position('update', request, id)
        if res:
            return render(request,'position.html',{'status':'success'})
        return bad_request(message='Can\'t Edit position at this moment')
    elif request.method == 'DELETE':
        res = manage_position('delete', request, id)
        if res:
            return render(request,'position.html',{'status':'success'})
        return bad_request(message='Can\'t delete position at this moment')