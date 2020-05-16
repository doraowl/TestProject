from HttpServer.models import *
from django.forms.models import model_to_dict
from django.core import serializers
def getAllPersons():
    return Person.objects.all()
