from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum
from django.contrib import messages


from api.forms import RegisterForm
from api.models import Employee, JobDetails, ProjectDetails
from recruitment.encrypt import encryption,decryption
from api.views.projects import get_object
from api.serializer.user_serializer import UserSerializer

@login_required(login_url='/login/')
def login_index(request):
    if len(request.user.groups.all()) != 0:
        return redirect('../home/')
    else:
        return redirect('../candidates/')

@login_required(login_url='/login/')
def rec_index(request):
    """This is for login"""
    employee = Employee.objects.get(msysemail=request.user)
    team_count = Employee.objects.filter(reporting_to=employee.emp_id,is_active=1).count()
    job_count = JobDetails.objects.filter(pm_emp_id=employee.emp_id, is_deleted=0 ,status=1).count()
    rmg_job_count = JobDetails.objects.filter(is_deleted=0 ,status=1,approved_by='HR').count()
    hr_job_count = JobDetails.objects.filter(is_deleted=0, status=1, approved_by='HR').count()
    openings_count = JobDetails.objects.filter(pm_emp_id=employee.emp_id,is_deleted=0,status=1).aggregate(Sum('no_of_positions'))
    billing_status= Employee.objects.filter(billing_status='bench').count()
    employee_count = Employee.objects.all().count()
    project_count = ProjectDetails.objects.filter(pm_emp_id=employee.emp_id).count()
    rmg_approval_pending = JobDetails.objects.filter(is_deleted=0, approved_by='RMG').count()
    return render(request, 'home.html', {
                                    'data':request.user,
                                    'count':dict(job_count=job_count,
                                    project_count=project_count,
                                    team_count=team_count,
                                    openings_count=openings_count['no_of_positions__sum'],
                                    billing_status=billing_status,
                                    rmg_job_count=rmg_job_count,
                                    hr_job_count=hr_job_count,
                                    employee_count=employee_count,
                                    rmg_approval_pending=rmg_approval_pending)
                            })


def registerform(request):
    """
    This is to register new user using django form
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = encryption(request.POST.get('password'))
            post.save()
            return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')    
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login/')
