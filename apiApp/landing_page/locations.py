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

#--------------------------- models -----------------------------------------------------
from apiApp.models import gallery_youtube
from apiApp.models import jeeyars
from apiApp.landing_page.landing_page_models import landing_page_flow
from apiApp.landing_page.landing_page_models import hero_section
from apiApp.landing_page.landing_page_models import banner_section
from apiApp.landing_page.landing_page_models import facebook_section
from apiApp.landing_page.landing_page_models import small_banner
from apiApp.landing_page.landing_page_models import card_section
from apiApp.landing_page.landing_page_models import suscribeModel


#------------------------start you views----------------------------------------------

@api_view(['POST'])
def countriesAll(request,format=None):
    try:
        df = pd.read_csv('locations.csv')
        country_list = list(df['country'].unique())
        res = {
                'status':True,
                'message':'country list',
                'country_count':len(country_list),
                'country_list':sorted(country_list)
            }
        return Response(res)
    except:
        res = {
                'status':False,
                'message':'something wend wrong',
            }
        return Response(res)


@api_view(['POST'])
def stateOfCountry(request,format=None):
    try:
        df = pd.read_csv('locations.csv')
        country = request.data['country']
        state_list = list(df.loc[(df['country'].isin([country]))]['state'].unique())
        print('####################',state_list)
        res = {
                'status':True,
                'message':'state list',
                'state_count':len(state_list) if type(state_list[0]) != float else 0,
                'state_list':sorted(state_list) if type(state_list[0]) != float else []
            }
        return Response(res)
    except:
        res = {
                'status':False,
                'message':'something wend wrong',
            }
        return Response(res)

@api_view(['POST'])
def cityOfCountryState(request,format=None):
    df = pd.read_csv('locations.csv')
    country = request.data['country']
    state = request.data['state']
    cities_list = list(df.loc[ (df['country'].isin([country])) & df['state'].isin([state]) ]['city'].unique())
    res = {
            'status':True,
            'message':'city list',
            'cities_count':len(cities_list) if type(cities_list[0]) != float else 0,
            'cities_list':sorted(cities_list) if type(cities_list[0]) != float else []
        }
    return Response(res)