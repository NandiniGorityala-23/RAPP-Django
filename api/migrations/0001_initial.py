# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 14:29
from __future__ import unicode_literals

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalDetails',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=20)),
                ('remarks', models.TextField()),
                ('file_upload', models.FileField(upload_to='documents/')),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=10, null=True)),
                ('rec_id', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('sur_name', models.CharField(max_length=255)),
                ('qualification', models.CharField(max_length=10)),
                ('year_of_passing', models.DateField(null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('department', models.CharField(max_length=100, null=True)),
                ('passport_no', models.CharField(max_length=100, null=True)),
                ('passport_doi', models.DateField(null=True)),
                ('passport_doe', models.DateField(null=True)),
                ('blood_group', models.CharField(max_length=20, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('doj', models.DateField(null=True)),
                ('msysemail', models.EmailField(max_length=254, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('file_upload', models.FileField(upload_to='doc/')),
                ('skill_set', models.TextField()),
                ('expected_ctc', models.CharField(max_length=20, null=True)),
                ('current_ctc', models.CharField(max_length=20, null=True)),
                ('notice_period', models.CharField(max_length=20, null=True)),
                ('hr_remarks', models.TextField()),
                ('rmg_remarks', models.TextField()),
                ('hr_approved', models.CharField(max_length=255)),
                ('approved_by', models.CharField(max_length=255)),
                ('date_time', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=255)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERS', 'Others')], default='Male', max_length=10)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married')], default='Single', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateFeedback',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('can_id', models.CharField(max_length=255)),
                ('ratings', models.CharField(max_length=255)),
                ('remarks', models.TextField()),
                ('skill_set', models.CharField(max_length=255)),
                ('file_upload', models.FileField(upload_to='documents/')),
                ('approved', models.BooleanField()),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientDetails',
            fields=[
                ('client_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('client_name', models.CharField(max_length=255)),
                ('client_location', models.CharField(max_length=255)),
                ('billing_entity', models.CharField(max_length=10, null=True)),
                ('MSA', models.TextField(null=True)),
                ('MSA_start_date', models.DateField(null=True)),
                ('MSA_end_date', models.DateField(null=True)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ClientRemarks',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('client_interviewer', models.CharField(max_length=255)),
                ('remarks', models.TextField()),
                ('file_upload', models.FileField(upload_to='documents/')),
                ('approved', models.BooleanField()),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=40)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=60, null=True)),
                ('name', models.CharField(max_length=60, null=True)),
                ('course', models.CharField(choices=[('REGULAR', 'regular'), ('DISTANCE', 'distance'), ('NOT REVELANT', 'not revelant')], default='regular', max_length=20)),
                ('emp_id', models.CharField(max_length=100, null=True)),
                ('doc_type', models.CharField(choices=[('WORD', 'word'), ('EXCEL', 'excel'), ('PDF', 'pdf'), ('JPEG', 'jpeg')], default='', max_length=20, null=True)),
                ('doc_file', models.CharField(max_length=100, null=True)),
                ('update_date', models.DateField()),
                ('remarks', models.CharField(max_length=100, null=True)),
                ('hr_remarks', models.CharField(max_length=100, null=True)),
                ('in_hand', models.CharField(choices=[('ORIGINAL', 'original'), ('COPY', 'copy')], default='original', max_length=20)),
                ('return_data', models.DateField()),
                ('verified', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=60)),
                ('msysemail', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('reporting_to', models.CharField(max_length=20)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('billing_status', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['slno'],
            },
        ),
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('rec_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('client_name', models.CharField(max_length=255)),
                ('no_of_positions', models.IntegerField()),
                ('experience', models.CharField(max_length=30)),
                ('qualification', models.CharField(max_length=30)),
                ('designation', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=30)),
                ('client_interview', models.BooleanField(default=False)),
                ('demand_type', models.CharField(max_length=100)),
                ('request_type', models.CharField(max_length=100)),
                ('skill_set', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('billable', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('approved_by', models.TextField()),
                ('job_description', models.TextField()),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('on_board_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('pm_emp_id', models.CharField(max_length=256)),
                ('interview_details', models.TextField()),
                ('interview_remarks', models.TextField()),
                ('is_deleted', models.IntegerField(default=0)),
                ('is_rejected', models.IntegerField(default=0)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('job_code', models.CharField(max_length=40)),
                ('job_type', models.CharField(max_length=40)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=30)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetails',
            fields=[
                ('project_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('projectname', models.CharField(max_length=255)),
                ('pm_emp_id', models.CharField(max_length=20)),
                ('SOW', models.CharField(max_length=255, null=True)),
                ('project_start_date', models.DateField(null=True)),
                ('project_end_date', models.DateField(null=True)),
                ('BU_head', models.CharField(max_length=255, null=True)),
                ('billing_type', models.CharField(max_length=50, null=True)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('client_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ClientDetails')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('qualification', models.CharField(max_length=40)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('request_type', models.CharField(max_length=40)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skillset',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=255)),
                ('skill_set', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=60)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('slno', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=255, unique=True)),
                ('user_name', models.CharField(max_length=100)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='project_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProjectDetails'),
        ),
        migrations.AddField(
            model_name='clientremarks',
            name='project_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProjectDetails'),
        ),
        migrations.AddField(
            model_name='clientremarks',
            name='rec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.JobDetails'),
        ),
        migrations.AddField(
            model_name='candidatefeedback',
            name='emp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Employee'),
        ),
        migrations.AddField(
            model_name='candidatefeedback',
            name='rec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.JobDetails'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='interviewer',
            field=models.ManyToManyField(to='api.Employee'),
        ),
        migrations.AddField(
            model_name='approvaldetails',
            name='rec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.JobDetails'),
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together=set([('emp_id', 'rec_id')]),
        ),
    ]
