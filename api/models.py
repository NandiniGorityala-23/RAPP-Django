from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime


class User(AbstractUser):
    """
    Extended django user model
    """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserAdmin(models.Model):

    """ To save admin username and password"""
    slno = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=255,unique=True)
    user_name = models.CharField(max_length=100)
    ts = models.DateTimeField(auto_now_add=True)
    
class ClientDetails(models.Model):
    
    """To save client details"""

    client_code = models.CharField(max_length=20,primary_key=True)
    client_name = models.CharField(max_length=255)
    client_location = models.CharField(max_length=255)
    billing_entity = models.CharField(max_length=10,null=True)
    MSA = models.TextField(null=True)
    MSA_start_date = models.DateField(auto_now_add=False,null=True)
    MSA_end_date = models.DateField(auto_now_add=False,null=True)
    ts = models.DateTimeField(auto_now_add=True)
    location= models.CharField(max_length=255)



class ProjectDetails(models.Model):
    
    """To save project details"""
    project_code = models.CharField(max_length=10,primary_key=True)
    client_code = models.ForeignKey(ClientDetails,on_delete=models.CASCADE)
    projectname = models.CharField(max_length=255)
    pm_emp_id = models.CharField(max_length=20)
    SOW = models.CharField(max_length=255,null=True)
    project_start_date = models.DateField(null=True)
    project_end_date = models.DateField(null=True)
    BU_head = models.CharField(max_length=255,null=True)
    billing_type = models.CharField(max_length=50,null=True)
    ts = models.DateTimeField(auto_now_add=True)


class JobDetails(models.Model):

    """To save job details"""
    rec_id = models.CharField(max_length=10,primary_key=True)
    project_code = models.ForeignKey(ProjectDetails,on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    no_of_positions = models.IntegerField()
    experience = models.CharField(max_length=30)
    qualification = models.CharField(max_length=40)
    designation = models.CharField(max_length=100)
    job_type = models.CharField(max_length=30)
    client_interview = models.BooleanField(default=False)
    demand_type = models.CharField(max_length=100)
    request_type = models.CharField(max_length=100)
    skill_set = models.TextField()
    location = models.CharField(max_length=255)
    billable = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    approved_by = models.TextField()
    # file_upload = models.FileField(upload_to = 'doc/')
    job_description=models.TextField()
    bill_date = models.DateField(auto_now_add=False,blank=True,null=True)
    on_board_date = models.DateField(auto_now_add=False,blank=True,default=datetime.now)
    pm_emp_id = models.CharField(max_length=256)
    interview_details = models.TextField()
    interview_remarks = models.TextField()
    is_deleted = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    ts = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateField(blank=True,null=True)



class Employee(models.Model):
    """ To get old employee details"""
    slno = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=100)
    name = models.CharField(max_length=60)
    msysemail = models.EmailField(max_length=254)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    reporting_to = models.CharField(max_length=20)
    ts = models.DateTimeField(auto_now_add=True)
    billing_status = models.CharField(max_length=10)


    class Meta:
        ordering = ['slno']

    def __str__(self):
        return '%s. %s-%s' % (self.slno, self.name, self.msysemail)

        
class Candidate(models.Model):

    """To save candidate details"""

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHERS = 'OTHERS'
    SINGLE = 'SINGLE'
    MARRIED = 'MARRIED'

    slno = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=10,null=True)
    rec_id = models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    sur_name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=10)
    year_of_passing = models.DateField(auto_now_add=False,null=True)
    designation = models.CharField(max_length=100,null=True)
    department = models.CharField(max_length=100,null=True)
    passport_no = models.CharField(max_length=100,null=True)
    passport_doi = models.DateField(auto_now_add=False,null=True)
    passport_doe = models.DateField(auto_now_add=False,null=True)
    blood_group = models.CharField(max_length=20,null=True)
    mobile = models.CharField(max_length=20,null=True)
    doj = models.DateField(auto_now_add=False,null=True)
    msysemail = models.EmailField(max_length=254,null=True)
    location = models.CharField(max_length=100,null=True)
    file_upload = models.FileField(upload_to = 'doc/')
    skill_set = models.TextField()
    expected_ctc = models.CharField(max_length=20,null=True)
    current_ctc = models.CharField(max_length=20,null=True)
    notice_period = models.CharField(max_length=20,null=True)
    interviewer = models.ManyToManyField(Employee)
    hr_remarks = models.TextField()
    rmg_remarks = models.TextField()
    hr_approved = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)
    date_time = models.CharField(max_length=30)
    status = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now_add=True)
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male',
    )
    MARITAL_CHOICES = (
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    )
    marital_status = models.CharField(
        max_length=10,
        choices=MARITAL_CHOICES,
        default='Single',
    )

    class Meta:
        unique_together = ('emp_id', 'rec_id',)

    
class ClientRemarks(models.Model):

    """To save client remarks"""

    slno = models.AutoField(primary_key=True)
    rec_id = models.ForeignKey(JobDetails,on_delete=models.CASCADE)
    project_code = models.ForeignKey(ProjectDetails,on_delete=models.CASCADE)
    client_interviewer = models.CharField(max_length=255)
    remarks = models.TextField()
    file_upload = models.FileField(upload_to='documents/')
    approved = models.BooleanField()
    ts = models.DateTimeField(auto_now_add=True)

class CandidateFeedback(models.Model):
    
    """To save interviewer remarks"""
    slno = models.AutoField(primary_key=True)
    rec_id = models.ForeignKey(JobDetails,on_delete=models.CASCADE)
    emp_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
    # project_code = models.ForeignKey(ProjectDetails,on_delete=models.CASCADE)
    can_id = models.CharField(max_length=255)
    ratings = models.CharField(max_length=255)
    remarks = models.TextField()
    skill_set = models.CharField(max_length=255)
    file_upload = models.FileField(upload_to='documents/')
    approved = models.BooleanField()
    ts = models.DateTimeField(auto_now_add=True)

class ApprovalDetails(models.Model):

    """To save approval details"""

    slno = models.AutoField(primary_key=True)
    rec_id = models.ForeignKey(JobDetails,on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20)
    remarks = models.TextField()
    file_upload = models.FileField(upload_to='documents/')
    ts = models.DateTimeField(auto_now_add=True)

class Skillset(models.Model):

    """To save employee skillset details"""
    
    slno = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=255)
    skill_set = models.CharField(max_length=255)
    experience = models.CharField(max_length=60)
    ts = models.DateTimeField(auto_now_add=True)

class Documents(models.Model):

    """To save Candidate Documents"""

    REGULAR = 'REGULAR'
    DISTANCE = 'DISTANCE'
    NOTREVELANT = 'NOT REVELANT'
    WORD = 'WORD'
    EXCEL = 'EXCEL'
    PDF = 'PDF'
    JPEG = 'JPEG'
    ORIGINAL = 'ORIGINAL'
    COPY = 'COPY'
    slno = models.AutoField(primary_key=True)
    code = models.CharField(max_length=60,null=True)
    name = models.CharField(max_length=60,null=True)
    COURSE_CHOICES = (
        (REGULAR, 'regular'),
        (DISTANCE, 'distance'),
        (NOTREVELANT, 'not revelant'),
    )
    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        default='regular',
    )
    emp_id = models.CharField(max_length=100,null=True)
    DOC_CHOICES = (
        (WORD, 'word'),
        (EXCEL, 'excel'),
        (PDF, 'pdf'),
        (JPEG, 'jpeg')
    )
    doc_type = models.CharField(
        max_length=20,
        choices=DOC_CHOICES,
        default='',
        null=True
    )
    doc_file = models.CharField(max_length=100,null=True)
    update_date = models.DateField(auto_now_add=False)
    remarks = models.CharField(max_length=100,null=True)
    hr_remarks = models.CharField(max_length=100,null=True)
    IN_HAND_CHOICES = (
        (ORIGINAL, 'original'),
        (COPY, 'copy'),
    )
    in_hand = models.CharField(
        max_length=20,
        choices=IN_HAND_CHOICES,
        default='original',
    )
    return_data = models.DateField(auto_now_add=False)
    verified = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    ts = models.DateTimeField(auto_now_add=True)

class Location(models.Model):

    """To save location like branches eg:chennai"""
    
    slno = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=30)
    ts = models.DateTimeField(auto_now_add=True)

class Qualification(models.Model):

    """To save Qualification eg:BCA"""
    
    slno = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=40)
    ts = models.DateTimeField(auto_now_add=True)

class Designation(models.Model):

    """To save Designation eg:senior software"""

    slno = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=40)
    ts = models.DateTimeField(auto_now_add=True)

class RequestType(models.Model):

    """To save job request type"""

    slno = models.AutoField(primary_key=True)
    request_type = models.CharField(max_length=40)
    ts = models.DateTimeField(auto_now_add=True)

class JobType(models.Model):

    """To save job Job type"""

    slno = models.AutoField(primary_key=True)
    job_code = models.CharField(max_length=40)
    job_type = models.CharField(max_length=40)
    ts = models.DateTimeField(auto_now_add=True)



