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
from apiApp.landing_page.landing_page_models import landing_page_flow
from apiApp.landing_page.landing_page_models import hero_section
from apiApp.landing_page.landing_page_models import banner_section
from apiApp.landing_page.landing_page_models import facebook_section
from apiApp.landing_page.landing_page_models import small_banner
from apiApp.landing_page.landing_page_models import card_section


#------------------------start you views----------------------------------------------

@api_view(['GET'])
def home_page(request,format=None):
    root_obj = landing_page_flow.objects.values()
    res = {}
    res['pageName'] = 'Home'
    all_sections = []

    c = 1  # banner_section
    d = 1  # small_banner 
    e = 1  # card_section
    for i in root_obj:
        single_section = {}
        single_section['section_name'] = 'Section '+ str(i['id'])
        single_section['layout'] = i['section_layout']
        single_section['status'] = i['show_status']
        single_section['id'] = i['id']
        
        if i['section_layout'] == 'hero_section':
            obj = hero_section.objects.values().last()
            section_data = [
                                {
                                    'id': 'h1',
                                    'title': "Heading",
                                    'content': obj['h1'],
                                    'type': "text",
                                    'section_data_status': True,
                                },
                                {
                                    'id': 'h2',
                                    'title': "Sub Heading",
                                    'content': obj['h2'],
                                    'type': "text",
                                    'section_data_status': True,
                                },
                                {
                                    'id': 'h3',
                                    'title': "Background Image",
                                    'content': obj['img'],
                                    'type': "bg_image",
                                    'section_data_status': True,
                                }
                            ]
            single_section['section_data'] = section_data
            all_sections.append(single_section)
        
        if i['section_layout'] == 'youtube_events':
            pass

        if i['section_layout'] == 'banner_section':
            obj = banner_section.objects.filter(section_id = i['id']).values()
            section_data = []
            for j in obj:
                if j['type'] == 'image':
                    section_data.append({
                                            'id': j['id'],
                                            'type': "image",
                                            'content': j['image'],
                                            'status':True
                                        })
                else:
                    section_data.append({
                                            'id': j['id'],
                                            'type': "text",
                                            'content_data': [
                                                                {
                                                                    'id': 'bcd'+str(c),
                                                                    'title': "Heading",
                                                                    'content': "21st Paasuram",
                                                                },
                                                                {
                                                                    'id': 'bcd'+str(c+1),
                                                                    'title': "Brief Info",
                                                                    'content':
                                                                    "Vanamamalai mutt",
                                                                },
                                                            ],
                                                'status':True
                                        })
                    c = c+2
            single_section['section_data'] = section_data
            all_sections.append(single_section)
        
        if i['section_layout'] == 'facebook_section':
            obj = facebook_section.objects.values().last()
            section_data = [
                            {
                                'id': 1,
                                'title': "Facebook Page Link",
                                'content': obj['link'],
                                'type': "text",
                                'section_data_status': True,
                            }
                         ]
            single_section['section_data'] = section_data
            all_sections.append(single_section)
            
        if i['section_layout'] == 'small_banner':
            obj = small_banner.objects.filter(section_id = i['id']).values().last()
            section_data = [
                                {
                                    'id': 'sb'+str(d),
                                    'title': "Heading",
                                    'content': obj['h1'],
                                    'type': "text",
                                    'section_data_status': True,
                                },
                                {
                                    'id':'sb'+str(d+1),
                                    'title': "Brief Info",
                                    'content': obj['p'],
                                    'type': "text",
                                    'section_data_status': True,
                                },
                                {
                                    'id': 'sb'+str(d+2),
                                    'title': "Cover Image",
                                    'content': obj['image'],
                                    'type': "image",
                                    'section_data_status': True,
                                },
                            ]
            d = d + 3
            single_section['section_data'] = section_data
            all_sections.append(single_section)
        
        if i['section_layout'] == 'card_section':
            obj = card_section.objects.filter(section_id = i['id']).values()
            section_data = []
            for j in obj:
                section_data.append({
                                        'card_id': j['id'],
                                        'card_data': [
                                                        {
                                                            'id': 'cs'+str(e),
                                                            'title': "Heading",
                                                            'content': j['h1'],
                                                            'type': "text",
                                                            'section_data_status': True,
                                                        },
                                                        {
                                                            'id': 'cs'+str(e+1),
                                                            'title': "Brief Info",
                                                            'content': j['p'],
                                                            'type': "text",
                                                            'section_data_status': True,
                                                        },
                                                    ],
                                    })
                e = e + 2
            single_section['section_data'] = section_data
            all_sections.append(single_section)

    res['all_sections'] = all_sections
    return Response(res)
            

    