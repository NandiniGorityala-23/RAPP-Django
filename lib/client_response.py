# other library
from recruitment.settings import DEBUG
from django.http import HttpResponse
import json

class ClientResponse():
    
    '''This is for formatting the response'''

    def response_formation(self, response):
        
        '''This is for formatting the response and returns it'''

        response_data = {}
        response_data['data'] =  response
        return (response_data)


def bad_request(message):
    response = HttpResponse(json.dumps({'message': message}), 
        content_type='application/json')
    response.status_code = 400
    return response