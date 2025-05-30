from django.core.management.base import BaseCommand, CommandError
import ast
from collections import namedtuple
from api.models import User


class Command(BaseCommand):
    help = 'Creating groups at initial stage'

    def handle(self, *args, **options):
        user_list_file = open('static\employeelist.txt', 'r')
        users_list_output = user_list_file.read().split('\n')
        for i in users_list_output:
            string = i.strip(', ')
            users_dict = ast.literal_eval(string)
            d = namedtuple('Employee', "emp_id name email")
            try:
                s = d(emp_id=users_dict['emp_id'], name=users_dict['name'], email=users_dict['email'])
                user = User(username=s.name, email=s.email)
                print(user)
                user.set_password('msys@123')
                user.save()
            except KeyError as e:
                s = d(emp_id=users_dict['emp_id'], name=users_dict['name'], email=users_dict['email'])
                print("Exception occured is", e)
        print("\n")
        print("Users Created Successfully")