from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django_ratelimit.decorators import ratelimit


#Definition of the view
# Best practice is to define the views for each user separately.
@ratelimit(key='ip', rate='10/m', method='GET', block=True) # Defined the rate limit in the decorator function.
def anonymous_login(request):
    """ 
    View to handle anonymous login requests.
    """
    return HttpResponse("Anonymous login attempt")

def authenticated_login(request):
    """ View to handle authenticated user requests"""
    return HttpResponse("Authenticated user login attempt")
