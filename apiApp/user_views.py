import numpy as np
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from operator import itemgetter 
import os
import random
import simplejson as json
#-------------------------Django Modules---------------------------------------------
from django.http import Http404, HttpResponse, JsonResponse,FileResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func,Q
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Min, Max
from django.db.models import Subquery
from django.db.models.functions import Lower, Replace
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes,api_view
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response

#------------------------start you views----------------------------------------------

@api_view(['POST'])
def login(request,format=ModuleNotFoundError):
    username = request.data['username']
    password = request.data['password']

    if username in ['amrit','vivek','admin']:
        if password == 'Vanama@312022':
            return Response(
                            {
                             'message':'Login Successfull',
                             'id':1,
                             'username':username,
                             'token':'token'
                            }
                            )
        else:
             return Response(
                            {
                             'message':'Invalid Credentials',
                            }
                            )
    else:
        return Response(
                            {
                             'message':'Invalid Credentials',
                            }
                            )