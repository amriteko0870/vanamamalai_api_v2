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

@api_view(['GET'])
def landing_page(request,format=None):
    landing_obj = landing_page_flow.objects.filter(show_status = True).values()
    res = []
    for i in landing_obj:
        if i['section_layout'] == 'hero_section':
            hero_res = {}
            hero_obj = hero_section.objects.values()
            hero_res['id'] = i['id']
            hero_res['layout'] = 'hero'
            # hero_res['h1'] = hero_obj['h1']
            # hero_res['h2'] = hero_obj['h2']
            # hero_res['img'] = hero_obj['img']
            hero_res['hero_data'] = list(hero_obj)[::-1]
            res.append(hero_res)
        

        if i['section_layout'] == 'youtube_events':
            youtube_res = {}
            youtube_obj = gallery_youtube.objects.annotate(yt_link = F('url'),yt_title = F('title')).values('yt_link','yt_title')
            youtube_res['id'] = i['id']
            youtube_res['layout'] = 'youtube_events'
            youtube_res['caraousel_data'] = list(youtube_obj)[::-1]
            res.append(youtube_res)

        if i['section_layout'] == 'banner_section':
            banner_res = {}

            banner_obj = banner_section.objects.filter(section_id = i['id'])
            banner_res['id'] = i['id']
            banner_res['layout'] = 'banner'
            banner_data = banner_obj.annotate(
                                                nid = Concat(
                                                                  V('BS-'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                            )
                                                
                                             ).values('nid','type','h1','p','image')
            banner_res['banner_data'] = banner_data
            res.append(banner_res)
        
        if i['section_layout'] == 'facebook_section':
            facebook_res = {}
            facebook_obj = facebook_section.objects.values().last()
            facebook_res['id'] = i['id']
            facebook_res['layout'] = 'facebook'
            facebook_res['fb_page_link'] = facebook_obj['link']
            res.append(facebook_res)
            
        if i['section_layout'] == 'jeeyar_list':
            jeeyar_list = {}
            jeeyar_list['id'] = i['id']
            jeeyar_list['call_link'] = "jeeyars_details"
            jeeyar_list['layout'] = "jeeyars"
            jeeyar = jeeyars.objects.filter(show_status = True).values('id','image','name','prefix','start_date','end_date','jeeyar_no','jeeyar_no_suffix')
            jeeyar_list['jeeyars'] = list(jeeyar)[::-1][:10]
            res.append(jeeyar_list)

        if i['section_layout'] == 'small_banner':
            small_banner_res = {}
            small_banner_obj = small_banner.objects.filter(section_id = i['id']).values().last()
            small_banner_res['id'] = i['id']
            small_banner_res['layout'] = 'small_banner'

            small_banner_res['image'] = small_banner_obj['image']
            small_banner_res['h1'] = small_banner_obj['h1']
            small_banner_res['p'] = small_banner_obj['p']
            res.append(small_banner_res)

        if i['section_layout'] == 'card_section':
            card_section_res = {}
            card_section_obj = card_section.objects.filter(section_id = i['id'])
            card_section_res['id'] = i['id']
            card_section_res['layout'] = 'cards'
            card_data = card_section_obj.values('h1','p')
            card_section_res['card_data'] = card_data
            res.append(card_section_res)    
    res = {
            'status':True,
            'data':res
          }
    return Response(res)



@api_view(['POST'])
def suscribeStore(request,format=None):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    phone_no = request.data['phone_no']
    email = request.data['email']

    data = suscribeModel(
                            first_name = first_name,
                            last_name = last_name,
                            phone_no = phone_no,
                            email = email,
                        )
    data.save()
    return Response({'status':True,'message':'Subscribed successfully'})

    

