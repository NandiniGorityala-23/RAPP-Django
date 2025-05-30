import smtplib
from smtplib import SMTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from lib.client_response import ClientResponse
from recruitment.email_config import EmailConfig

res_obj = ClientResponse()

class SendMail(APIView):
	"""docstring for SendMail"""

	def post(self, request, format=None):
		"""docstring for post"""
		email = EmailConfig()
		try:
			to_mail = request.data.get('email')
			smtpserver = smtplib.SMTP(email.EMAIL_HOST,email.EMAIL_PORT)
			smtpserver.ehlo()
			if email.USE_SSL_TL:
				smtpserver.starttls()
				smtpserver.ehlo() # extra characters to permit edit
				smtpserver.login(email.FROM_MAIL, email.EMAIL_HOST_PASSWORD)

			smtpserver.ehlo()
			header = 'To:' + to_mail + '\n' + 'From: ' + email.FROM_MAIL + '\n' + 'Subject:Recruitment App \n'
			message = header + '\n This is RecruitmentApp test mail  \n\n'
			smtpserver.sendmail(email.FROM_MAIL, to_mail, message)
			smtpserver.quit()
			(response, status_code) = res_obj.response_formation("mail sent", status.HTTP_200_OK)
			return Response(response, status=status_code)

		except Exception as e:
			(response, status_code) = res_obj.response_formation(str(e), status.HTTP_400_BAD_REQUEST)
			return Response(response, status=status_code)