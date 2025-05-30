from django.conf.urls import include, url

from api.views.mail import SendMail
from api.views.projects import get_projects,get_client
from api.views.positions import position_list, position_detail, get_skills,get_employee
from api.views.approvals import get_approvals,get_rec_approvals,get_rgm_approvals
from api.views.hrapprovals import get_hr_approvals,get_rechr_approvals,addnewcandidate,interviewer
from api.views.oauth import rec_index, login_index
from api.views.candidates import get_candidates,feedback,get_feedback,update_candidate_remarks,\
                                 approved_candidates,hrapproved_candidates, hr_approved_candidates
from api.views.teammembers import get_team_member
from api.views.profile import  get_profile
from  api.views.change_password import  change_password
from api.views.addclient import add_client

urlpatterns = [
    # test mail send
    url(r'^projects/(?P<client_code>[\w\-]+)/$', get_projects, name='projects'),
    url(r'^home/$', rec_index, name='home'),
    url(r'^index/$', login_index, name='login_index'),
    url(r'^clients/$', get_client, name='client'),
    url(r'^mail/$', SendMail.as_view()),
    url(r'^position/$', position_list, name='position_list'),
    url(r'^position/(?P<id>[\w\-]+)/$', position_detail, name='position_detail'),
    url(r'^addnewcandidate/(?P<rec_id>[\w\-]+)/$', addnewcandidate, name='addnewcandidate'),
    url(r'^interviewer/(?P<can_id>[\w\-]+)/$',interviewer, name='interviewer'),
    url(r'^skillset/$', get_skills, name='skills'),
    url(r'^employee/$', get_employee, name='employee'),
    url(r'^approvals/$', get_approvals, name='approvals'),
    url(r'^approvals/(?P<rec_id>[\w\-]+)/$',get_rec_approvals, name='rec_approvals'),
    url(r'^myapprovals/$',get_rgm_approvals, name='rgm_approvals'),
    url(r'^hrapprovals/$',get_hr_approvals, name='hr_approvals'),
    url(r'^hrapprovals/(?P<rec_id>[\w\-]+)/(?P<type>[\w\-]+)$',get_rechr_approvals, name='get_rechr_approvals'),
    url(r'^candidates/$',get_candidates, name='get_candidates'),
    url(r'^candidate/(?P<can_id>[\w\-]+)/$',update_candidate_remarks, name='update_candidate_remarks'),
    url(r'^feedback/$',feedback, name='get_feedback'),
    url(r'^feedback/(?P<can_id>[\w\-]+)/$',get_feedback, name='candidate_feedback'),
    url(r'^hrapprovedcandidates/$',hrapproved_candidates, name='hrapproved_candidates'),
    url(r'^hrapprovedcandidates/(?P<rec_id>[\w\-]+)/$',hr_approved_candidates, name='hr_approved_candidates'),
    url(r'^approvedcandidates/(?P<rec_id>[\w\-]+)/$',approved_candidates, name='approved_candidates'),
    url(r'^teammembers/$',get_team_member,name='get_team_member'),
    url(r'^profile/$',get_profile,name='get_profile'),
    url(r'^password/$',change_password, name='change_password'),
    url(r'^addclient/$',add_client, name='add_client'),
]