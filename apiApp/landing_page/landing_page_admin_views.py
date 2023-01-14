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

# ---------------------------- extra ---------------------------------------------------
from apiApp.admin_pages.image_upload import image_upload
#------------------------start you views----------------------------------------------

@api_view(['GET','PUT','PATCH'])
def home_page(request,format=None):
    if request.method == 'GET':
        root_obj = landing_page_flow.objects.values()
        res = {}
        res['pageName'] = 'Home'
        all_sections = []

        c = 1  # banner_section
        d = 1  # small_banner 
        e = 1  # card_section
        s = 1  # section_count
        for i in root_obj:
            single_section = {}
            single_section['section_name'] = 'Section '+ str(s)
            single_section['layout'] = i['section_layout']
            single_section['status'] = i['show_status']
            single_section['id'] = i['id']
            
            if i['section_layout'] == 'hero_section':
                obj = hero_section.objects.values()
                section_data = []
                for j in obj:
                    section_data.append({
                                        'id': j['id'],
                                        'content': j['img'],
                                        'type': "image",
                                        'section_data_status': True,
                                        })
                                    
                                
                single_section['section_data'] = section_data[::-1]
                all_sections.append(single_section)
                s = s + 1
            
            if i['section_layout'] == 'youtube_events':
                pass

            if i['section_layout'] == 'banner_section':
                obj = banner_section.objects.filter(section_id = i['id']).values()
                section_data = []
                for j in obj:
                    section_data.append({
                                            'id': j['id'],
                                            'type': j["type"],
                                            'content': j['image'],
                                            'content_data': [
                                                                {
                                                                    'id': 'bcd'+str(c),
                                                                    'title': "Heading",
                                                                    'content': j['h1'],
                                                                },
                                                                {
                                                                    'id': 'bcd'+str(c+1),
                                                                    'title': "Brief Info",
                                                                    'content':j['p'],
                                                                },
                                                            ],
                                            'status':True
                                        })
                    c = c+2
                single_section['section_data'] = section_data
                all_sections.append(single_section)
                s = s + 1
            
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
                s = s + 1
                
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
                s = s + 1
            
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
                s = s + 1
        res['all_sections'] = all_sections
        return Response(res)
        
    if request.method == 'PUT':
        data = request.data
        main_obj = landing_page_flow.objects.values()
        
        for i in data['all_sections']:
            main_obj.filter(id = i['id']).update(show_status = i['status'])
            if i['layout'] == 'hero_section':
                for j in i['section_data']:
                    hero_section.objects.filter(id = j['id']).update(img = j['content'])

            if i['layout'] == 'banner_section':
                for j in i['section_data']:
                    banner_section.objects.filter(id = j['id'])\
                                        .update(
                                                    type = j['type'],
                                                    h1 = j['content_data'][0]['content'],
                                                    p = j['content_data'][0]['content'],
                                                    image = j['content'],
                                               )
            
            if i['layout'] == 'facebook_section':
                facebook_section.objects.filter(id = i['id'])\
                                        .update(
                                                link = i['section_data'][0]['content']
                                        )
            
            if i['layout'] == 'small_banner':
                small_banner.objects.filter(id = i['id'])\
                                    .update(
                                                h1 = i['section_data'][0]['content'],
                                                p = i['section_data'][1]['content'],
                                                image = i['section_data'][2]['content'],
                                            )
            
            if i['layout'] == 'card_section':
                for j in i['section_data']:
                    card_section.objects.filter(id = j['card_id'])\
                                        .update(
                                                    h1 = j['card_data'][0]['content'],
                                                    p = j['card_data'][1]['content'],
                                                )
        return Response({'status':True,'message':'Publish successfull'})

    if request.method == 'PATCH':
        section_id = request.data['data']['id']
        obj = landing_page_flow.objects.filter(id = section_id).values()
        if obj.last()['show_status'] :
            obj.update(
                        show_status = False
                      )
        else:
            obj.update(
                        show_status = True
                      )
        return Response({'status':True,'message':'Status changed successfully'})
        
    

@api_view(['POST','DELETE'])
def hero_section_admin(request,format = None):
    if request.method == 'POST':
        file = request.FILES['file']
        img_path = 'img/'
        upload_res = image_upload(file,img_path)
        updated_value = 'media/'+upload_res
        data = hero_section(
                            img = updated_value
                           )
        data.save()
        return Response({'status':True,'message':'Upload successfull'})
    
    if request.method == 'DELETE':
        img_id = request.data['id']
        hero_section.objects.filter(id = img_id).delete()
        return Response({'status':True,'message':'Delete successfull'})

    
@api_view(['POST'])
def bannerTypeChange(request,format=None):
    banner_id = request.data['id']
    new_type = request.data['type']
    banner_section.objects.filter(id = banner_id).update(type = new_type)
    return Response({'status':True,'message':'Type changed successfully'})
