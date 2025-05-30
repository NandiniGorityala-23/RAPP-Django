import datetime
import uuid
import json
from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from api.models import  ClientDetails,Qualification,Designation,RequestType,Location,\
                        JobType,JobDetails,ProjectDetails,Employee,Skillset,Candidate
from api.serializer.position_serializer import SkillSerializer,EmployeeSerializer,JobSerializer
from api.serializer.projects_serializer import ProjectDetailsSerializer,ClientDetailsSerializer
from api.serializer.user_serializer import UserSerializer
from lib.client_response import ClientResponse
from lib.decorators import group_required

res_obj = ClientResponse()


@ensure_csrf_cookie
@api_view(['GET'])
@group_required('RMG')
def get_approvals(request):
    """
    This is to register new user using django form
    """
    response = OrderedDict({})
    projects = ProjectDetails.objects.all()
    for project in projects:
        jobs = JobDetails.objects.filter(project_code=project.project_code, is_deleted=0, approved_by='RMG')
        employee = Employee.objects.filter(emp_id=project.pm_emp_id)
        client = ClientDetails.objects.filter(client_code=project.client_code.client_code)
        if not response.get(str(project.client_code.client_code),None):
            response[str(project.client_code.client_code)] = {}

        if not response[str(project.client_code.client_code)].get(project.pm_emp_id, None):
            response[str(project.client_code.client_code)][project.pm_emp_id]=[]
        for emp in employee:
            for job in jobs:
                # candidates = Candidate.objects.filter(rec_id=job.rec_id, hr_approved=1).count()
                rec = {
                        'rec_id':job.rec_id, 
                        'project_name':project.projectname,
                        'rec_date':job.ts.strftime("%d/%m/%Y"),
                        # 'designation':job.designation,
                        'request_type':job.request_type,
                        'no_of_positions':job.no_of_positions,
                        'status':job.status,
                        'skills':job.skill_set,
                        'approved_by':job.approved_by,
                        'employee_name':emp.name,
                        'client_name':str(project.client_code.client_name),
                        # 'selected_candidate_count':candidates
                        }
                response[str(project.client_code.client_code)][project.pm_emp_id].append(rec)

    # return Response(response)

    return render(request, 'approvals.html',{'data':request.user,'response':response})


@ensure_csrf_cookie
@api_view(['GET','PUT'])
@login_required(login_url='/login/')
def get_rec_approvals(request, rec_id,format=None):
    job_details = JobDetails.objects.filter(rec_id=rec_id, is_deleted=0)
    response = []
    job_dict={}
    if request.method == 'GET':
        for job in job_details:
            proj = ProjectDetails.objects.get(project_code=job.project_code_id)
            job_dict['no_of_positions']=job.no_of_positions
            job_dict['experience']=job.experience
            job_dict['qualification']=job.qualification
            job_dict['location']=job.location
            job_dict['demand_type']=job.demand_type
            job_dict['client_interview']=job.client_interview
            job_dict['billable']=job.billable
            job_dict['job_type']=job.job_type
            job_dict['job_description']=job.job_description
            job_dict['designation']=job.designation
            job_dict['approved_by']=job.approved_by
            job_dict['interview_det']=job.interview_details
            job_dict['client_name']=job.client_name
            job_dict['project_code']=job.project_code_id
            job_dict['project_name']=proj.projectname
            job_dict['request_type']=job.request_type
            job_dict['skills']=map(lambda x: x.strip(), job.skill_set.split(','))
            job_dict['interview_det']=map(lambda x: x.strip(), job.interview_details.split(','))
            if (job.bill_date):
                job_dict['bill_date']=datetime.datetime.strptime(str(job.bill_date), "%Y-%m-%d").strftime("%d/%m/%Y")
            else:
                job_dict['bill_date'] = ''   
            
            # job_dict['interview_details_id']=job.interview_details
            emp_name = ''
            for emp in job.interview_details.split(","):
                employee = Employee.objects.filter(emp_id=emp.strip())
                for name in employee:
                    emp_name += emp+'-'+name.name+'\n'
                    job_dict['interview_details']=emp_name.strip(',')
            
            response.append(job_dict)
        res = res_obj.response_formation(response)
        return Response(res)

    if request.method == 'PUT':
        job = JobDetails.objects.get(rec_id=rec_id)
        if (str(request.data.get('status'))=='0'):      
            job.approved_by='Initiator'
            job.is_rejected=1
        else:
            job.approved_by='HR'
        job.interview_remarks =request.data.get('name')
        job.save()
        # response = res_obj.response_formation({'message':'Approved successfully'})
        response = {'message':'Approved successfully'}
        return Response(response)
    # return render(request, 'approvals.html',{'data':request.user,'response':res})


@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def get_rgm_approvals(request, format=None):
    """
    This is to register new user using django form
    """
    response = OrderedDict({})
    projects = ProjectDetails.objects.all()
    for project in projects:
        jobs = JobDetails.objects.filter(project_code=project.project_code,approved_by="HR", is_deleted=0)
        employee = Employee.objects.filter(emp_id=project.pm_emp_id)
        client = ClientDetails.objects.filter(client_code=project.client_code.client_code)
        if not response.get(str(project.client_code.client_code),None):
            response[str(project.client_code.client_code)] = {}

        if not response[str(project.client_code.client_code)].get(project.pm_emp_id, None):
            response[str(project.client_code.client_code)][project.pm_emp_id]=[]
        for emp in employee:
            for job in jobs:
                candidates = Candidate.objects.filter(rec_id=job.rec_id)
                rec = {
                        'rec_id':job.rec_id, 
                        'project_name':project.projectname,
                        'rec_date':job.ts.strftime("%d/%m/%Y"),
                        # 'designation':job.designation,
                        'request_type':job.request_type,
                        'no_of_positions':job.no_of_positions,
                        'status':job.status,
                        'skills':job.skill_set,
                        'approved_by':job.approved_by,
                        'employee_name':emp.name,
                        'client_name':str(project.client_code.client_name),
                        'selected_candidate_count':candidates.filter(hr_approved=1, status='SELECTED').count(),
                        'approved_candidate_count':candidates.filter(hr_approved=1, status='APPROVED').count()
                        }
                response[str(project.client_code.client_code)][project.pm_emp_id].append(rec)

    # return Response(response)

    return render(request, 'approvals.html',{'data':request.user,'response':response})
