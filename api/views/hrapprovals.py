from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from django.shortcuts import render
# import ast
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError

from lib.client_response import ClientResponse, bad_request
from api.models import  ClientDetails,Qualification,Designation,RequestType,Location,\
                        JobType,JobDetails,ProjectDetails,Employee,Skillset,Candidate,\
                        CandidateFeedback
from api.serializer.position_serializer import SkillSerializer,EmployeeSerializer,JobSerializer
from api.serializer.projects_serializer import ProjectDetailsSerializer,ClientDetailsSerializer
from api.serializer.user_serializer import UserSerializer
from api.serializer.candidatefeedback_serializer import CandidateFeedbackSerializer
import datetime
import uuid

from collections import OrderedDict

res_obj = ClientResponse()


@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def get_hr_approvals(request, format=None):
    """
    This is to register new user using django form
    """
    response = OrderedDict({})
    projects = ProjectDetails.objects.all()
    for project in projects:
        jobs = JobDetails.objects.filter(project_code=project.project_code, approved_by="HR", is_deleted=0)
        employee = Employee.objects.filter(emp_id=project.pm_emp_id).first()
        client = ClientDetails.objects.filter(client_code=project.client_code.client_code)
        if not response.get(str(project.client_code.client_code),None):
            response[str(project.client_code.client_code)] = {}

        if not response[str(project.client_code.client_code)].get(project.pm_emp_id, None):
            response[str(project.client_code.client_code)][project.pm_emp_id]=[]
        
        for job in jobs:
            candidate_count = Candidate.objects.filter(rec_id=job.rec_id).count()
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
                    'employee_name':employee.name,
                    'client_name':str(project.client_code.client_name),
                    'candidate_count': candidate_count,
                }
            response[str(project.client_code.client_code)][project.pm_emp_id].append(rec)
    # return Response(response)

    return render(request, 'hrapprovals.html',{'data':request.user,'response':response})

@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def get_rechr_approvals(request,rec_id,type,format=None):
    """
    This is to register new user using django form
    """
    job_details = JobDetails.objects.filter(rec_id=rec_id, is_deleted=0)
    candidate_details = Candidate.objects.filter(rec_id=rec_id)
    response = []
    job_dict={}
    if request.method == 'GET':
        for job in job_details:
            job_dict['rec_id']=job.rec_id
            proj = ProjectDetails.objects.get(project_code=job.project_code.project_code)
            client = ClientDetails.objects.get(client_code=job.client_name)
            employee = Employee.objects.get(emp_id=proj.pm_emp_id)
            job_dict['client']=client.client_name
            job_dict['pm_name']=employee.name
            job_dict['project']=proj.projectname
            job_dict['no_of_positions']=job.no_of_positions
            job_dict['experience']=job.experience
            job_dict['request_type']=job.request_type
            job_dict['qualification']=job.qualification
            job_dict['designation']=job.designation
            job_dict['rec_date']=job.ts.strftime("%d/%m/%Y")
            job_dict['skill_set']=job.skill_set
            job_dict['selected_candidate_count'] = candidate_details.filter(status='SELECTED').count()
        candidates = []
        for candidate in candidate_details:
            c_id = candidate.slno
            interview_details = candidate.interviewer.all()
            feebacks_count = CandidateFeedback.objects.filter(can_id=c_id).count()
            # employee_serializer = EmployeeSerializer(candidate.interviewer.all(), many=True)
            # interview_details = employee_serializer.data
            # feedbacks = CandidateFeedback.objects.filter(can_id=c_id)
            # interview_remarks = CandidateFeedbackSerializer(feedbacks, many=True).data
            candidates.append(
                                dict( 
                                    c_id = c_id, 
                                    emp_id = candidate.emp_id, 
                                    name=candidate.name,
                                    skill_set=candidate.skill_set,
                                    notice_period=candidate.notice_period,
                                    current_ctc=candidate.current_ctc,
                                    expected_ctc=candidate.expected_ctc,
                                    file_upload=str(candidate.file_upload),
                                    interview_details = interview_details,
                                    can_feedback_cnt = feebacks_count,
                                    hr_approved = candidate.hr_approved,
                                    status = candidate.status
                                )
                            )
        job_dict['candidates'] = candidates
        response.append(job_dict)
        res = res_obj.response_formation(response)

    # return Response(res)
    return render(request, 'hrcandidate.html',{ 'data':request.user, 'response':res,'type':type})

@login_required(login_url='/login/')
def addnewcandidate(request, rec_id,format=None):
    """
    This is to add new Candidate
    """
    candidate=Candidate()
    if request.method == 'POST':

        if request.FILES.has_key('file_upload'):
            myfile = request.FILES['file_upload']
            fs = FileSystemStorage()
            unique_file_name=uuid.uuid1()
            filename = fs.save(str(unique_file_name), myfile)
            uploaded_file_url = fs.url(filename) 
        else:
            unique_file_name = None

        skillset = json.loads(request.POST.get('skills'))
        skillset_data = ', '.join(skillset)

        # if request.POST.get('interview_det') or request.POST.get('interview_remarks'):
        #     interview_details = json.loads(request.POST.get('interview_det'))
        #     interview_remarks = request.POST.get('interview_remarks')
        #     interview_data = ','.join(interview_details)
        # else:
        #     interview_data = ""
        #     interview_remarks = ""

        job = JobDetails.objects.filter(rec_id=rec_id, is_deleted=0).first()
            
        candidate.rec_id = rec_id
        candidate.emp_id = request.POST.get('emp_id')
        candidate.name = request.POST.get('emp_name')
        candidate.skill_set = skillset_data
        candidate.qualification = job.qualification
        candidate.designation = job.designation
        candidate.current_ctc = request.POST.get('current_ctc')
        candidate.expected_ctc = request.POST.get('expected_ctc')
        candidate.notice_period = request.POST.get('notice_period')
        candidate.file_upload =str(unique_file_name)
        try:
            candidate.save()
        except IntegrityError as e:
            return bad_request(message="Employee id %s already exists" % request.POST.get('emp_id'))

        for emp_id in job.interview_details.split(','):
            employee = Employee.objects.get(emp_id=emp_id.strip())
            candidate.interviewer.add(employee)

        return render(request,'hrcandidate.html',{'status':'success'})

    if request.method == 'PUT':
        value = json.loads(request.body)
        candidate = Candidate.objects.get(slno=value.get('can_id'))
        # interview_data = ','.join(value.get('interview_det'))
        if value.get('role'):
            candidate.notice_period = value.get('notice_period')
            candidate.current_ctc = value.get('current_ctc')
            candidate.expected_ctc = value.get('expected_ctc')

        if value.get('status'):
            if int(value.get('status')):
                candidate.status = 'SELECTED'
            else:
                candidate.status = 'REJECTED'
        if value.get('rmg_remarks'):
            candidate.rmg_remarks = value.get('rmg_remarks')
        candidate.save()

        if candidate.status == 'SELECTED':
            job = JobDetails.objects.filter(rec_id= candidate.rec_id, is_deleted=0).first()
            no_of_positions  = int(job.no_of_positions)
            selected_candidate_count = Candidate.objects.filter(rec_id=rec_id, status='SELECTED').count()
            if selected_candidate_count >= no_of_positions:
                job.status = False
                job.approved_by = ""
                job.closed_at = datetime.datetime.now().date()
                job.save()

        if value.get('interview_det'):
            # clear a existing interviewer details
            candidate.interviewer.clear()
            for emp_id in value.get('interview_det'):
                employee = Employee.objects.get(emp_id=emp_id.strip())
                candidate.interviewer.add(employee)

        if value.get('date_time'):
            candidate.date_time = value.get('date_time')
        candidate.save()

        return render(request,'hrcandidate.html',{'status':'success'})
    else:
        return render(request,'hrcandidate.html',{'status':'error'})


@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def interviewer(request,can_id):
    candidate = Candidate.objects.get(slno=can_id)
    interviewer_names=[]

    if candidate.interview_details:
        for emp_id in candidate.interview_details.split(","):
            employee = Employee.objects.filter(emp_id=emp_id).first()
            emp_name = emp_id+'-'+employee.name
            interviewer_names.append(emp_name)
    response = res_obj.response_formation(interviewer_names)
    return Response(response)
