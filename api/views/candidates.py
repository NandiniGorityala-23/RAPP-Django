from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.shortcuts import render
from lib.client_response import ClientResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from api.models import  ClientDetails,Qualification,Designation,RequestType,Location,\
                        JobType,JobDetails,ProjectDetails,Employee,Skillset,\
                        Candidate,CandidateFeedback


from api.serializer.candidatefeedback_serializer import CandidateFeedbackSerializer
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
import json
import uuid
from django.http import HttpResponse
import  datetime

res_obj = ClientResponse()

@api_view(['GET'])
@login_required(login_url='/login/')
def get_candidates(request):
    interviewer = Employee.objects.filter(msysemail=request.user.email).first()
    rec_ids = [job.rec_id for job in JobDetails.objects.filter(is_deleted=0).filter(status=True)]
    interviewer_candidate = interviewer.candidate_set.filter(hr_approved='', rec_id__in=rec_ids)
    return render(request, 'candidate.html',{'data':request.user,'candidates':interviewer_candidate})


@login_required(login_url='/login/')
def feedback(request):
    interviewer = Employee.objects.filter(msysemail=request.user.email).first() 
    feedback = CandidateFeedback()
    if request.method == 'POST':
        job_det = JobDetails.objects.filter(rec_id=str(request.POST.get('rec_id'))).first()
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
        feedback.emp_id=interviewer
        feedback.can_id=request.POST.get('can_id')  
        feedback.remarks =request.POST.get('candidate_comments')    
        feedback.approved =request.POST.get('candidate_status')   
        feedback.rec_id  =job_det
        feedback.ratings  =request.POST.get('candidate_ratings') 
        feedback.skill_set  =skillset_data 
        feedback.file_upload =str(unique_file_name)
        feedback.save()
    return render(request, 'candidate.html',{'status':'success'})

@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def get_feedback(request,can_id,format=None):
    """
    This is to getting patricular candidate feedback
    """
    candidate=Candidate.objects.filter(slno=can_id).first()
    emp_ids=[emp.emp_id for emp in candidate.interviewer.all()]
    feed_back = CandidateFeedback.objects.filter(can_id=can_id)
    res_dict = {}
    response = []
    for candidate_feedback in feed_back:
        feedback_dict={}
        feedback_dict['can_id']=candidate_feedback.can_id
        feedback_dict['emp_id']=candidate_feedback.emp_id.emp_id
        feedback_dict['emp_name']=candidate_feedback.emp_id.name
        feedback_dict['remarks']=candidate_feedback.remarks
        feedback_dict['approved']=candidate_feedback.approved
        feedback_dict['ratings']=candidate_feedback.ratings
        feedback_dict['skill_set']=candidate_feedback.skill_set
        feedback_dict['ts'] = datetime.datetime.strptime(
            str(candidate_feedback.ts).split()[0], "%Y-%m-%d").strftime("%d-%m-%Y")
        feedback_dict['file']=str(candidate_feedback.file_upload)
        response.append(feedback_dict)
        
    res_dict['feedbacks'] = response
    res_dict['interviewer_details'] = emp_ids
    res = res_obj.response_formation(res_dict)
    return Response(res)

@ensure_csrf_cookie
@api_view(['PUT'])
@login_required(login_url='/login/')
def update_candidate_remarks(request,can_id,format=None):
    candidate = Candidate.objects.get(slno=str(can_id))
    hr = Employee.objects.filter(msysemail=request.user.email).first()
    candidate.hr_approved = request.POST.get('candidate_status')
    candidate.hr_remarks = request.POST.get('candidate_comments')
    candidate.approved_by = hr.emp_id
    if int(request.POST.get('candidate_status')):
        candidate.status = "APPROVED"
    else:
        candidate.status = "REJECTED"
    msg="Candidate %s Successfully" %candidate.status
    candidate.save()
    return HttpResponse(json.dumps({'msg': msg.title()}))
        
@api_view(['GET'])
@login_required(login_url='/login/')
def approved_candidates(request,rec_id):
    candidates = Candidate.objects.filter(rec_id=rec_id,hr_approved=1, status='SELECTED')
    return render(request, 'candidate.html',{'data':request.user,'candidates':candidates})

@api_view(['GET'])
@login_required(login_url='/login/')
def hr_approved_candidates(request,rec_id):
    candidates = Candidate.objects.filter(rec_id=rec_id,hr_approved=1, status='APPROVED')
    return render(request, 'candidate.html',{'data':request.user,'candidates':candidates})

@ensure_csrf_cookie
@api_view(['GET'])
@login_required(login_url='/login/')
def hrapproved_candidates(request,format=None):
    """
    This is to register new user using django form
    """
    # print '#'*80
    response = OrderedDict({})
    projects = ProjectDetails.objects.all()
    for project in projects:
        jobs = JobDetails.objects.filter(project_code=project.project_code,is_deleted=0)
        pm = Employee.objects.get(emp_id=project.pm_emp_id)
        client = ClientDetails.objects.filter(client_code=project.client_code.client_code)
        if not response.get(str(project.client_code.client_code),None):
            response[str(project.client_code.client_code)] = {}

        if not response[str(project.client_code.client_code)].get(project.pm_emp_id, None):
            response[str(project.client_code.client_code)][project.pm_emp_id]=[]

        for job in jobs:
            candidate_count = Candidate.objects.filter(rec_id=job.rec_id,hr_approved=1).count()
            if candidate_count:
                rec = {
                        'rec_id':job.rec_id, 
                        'project_name':project.projectname,
                        'rec_date':job.ts.strftime("%d/%m/%Y"),
                        # 'designation':job.designation,
                        'request_type':job.request_type,
                        'status':job.status,
                        'skills':job.skill_set,
                        'approved_by':job.approved_by,
                        'employee_name':pm.name,
                        'client_name':str(project.client_code.client_name),
                        'selected_candidate_count':candidate_count
                        }
                response[str(project.client_code.client_code)][project.pm_emp_id].append(rec)

    # return Response(response)

    return render(request, 'approvals.html',{'data':request.user,'response':response})