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
from PIL import Image  
import PIL  
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

#----------------------------models---------------------------------------------------
from apiApp.models import landing_page,vanamamalai_temple,vanamamalai_temple_tab
from apiApp.models import gallery,gallery_album,gallery_details,gallery_youtube
from apiApp.models import jeeyars,jeeyars_tab
from apiApp.models import vanamamalai_other_temple,vanamamalai_other_temple_tab
from apiApp.models import vanamamalai_mutt_branches,vanamamalai_mutt_branches_tab
from apiApp.models import ponnadikkal_jeeyar,ponnadikkal_jeeyar_tab
from apiApp.models import vanamamalai_education,vanamamalai_education_tab
from apiApp.models import rootPageStatus

#--------------------------- extra -------------------------------------------------
from apiApp.admin_pages.image_upload import image_upload
from apiApp.admin_pages.layout import layoutCreation,addTab
#---------------------------------------- start your views -----------------------------------------------

@api_view(['POST','PATCH'])
def adminDashboard(request,format=None):
   if request.method == 'POST':
      obj = rootPageStatus.objects.values()

      res = {}
      res['title'] = ["Page title", " Side pages", "Status", "Actions"]
      data = []   

      home = {
               'page_name':'Home Page',
               'page_link':'/admin/home_edit',
               'status':True
            }
      data.append(home)

      vm_temple_data = {
                           'id':obj.filter(title__iexact = 'Vanamamalai temple').values_list('id',flat=True).last(),
                           'page_name':'Vanamamalai temple',
                           'sub_pages':vanamamalai_temple.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Vanamamalai temple').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/vn_temple_edit/'
                        }
      data.append(vm_temple_data)

      other_temple_data = {
                           'id':obj.filter(title__iexact = 'Other temple').values_list('id',flat=True).last(),
                           'page_name':'Other temple',
                           'sub_pages':vanamamalai_other_temple.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Other temple').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/other_temple_edit'
                        }
      data.append(other_temple_data) 

      branches_data = {
                           'id':obj.filter(title__iexact = 'Branches').values_list('id',flat=True).last(),
                           'page_name':'Branches',
                           'sub_pages':vanamamalai_mutt_branches.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Branches').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/branches_edit'
                        }
      data.append(branches_data) 

      ponnadikkal_jeeyar_data = {
                           'id':obj.filter(title__iexact = 'Ponnadikkal Jeeyar').values_list('id',flat=True).last(),
                           'page_name':'Ponnadikkal Jeeyar',
                           'sub_pages':ponnadikkal_jeeyar.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Ponnadikkal Jeeyar').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/ponnadikkal_jeeyar_edit/'+str(ponnadikkal_jeeyar.objects.values().last()['id'])
                        }
      data.append(ponnadikkal_jeeyar_data)   

      jeeyar_data = {
                           'id':obj.filter(title__iexact = 'Jeeyars').values_list('id',flat=True).last(),
                           'page_name':'Jeeyars',
                           'sub_pages':jeeyars.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Jeeyars').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/jeeyars_edit'
                        }
      data.append(jeeyar_data)   
   
      education_data = {
                           'id':obj.filter(title__iexact = 'Education').values_list('id',flat=True).last(),
                           'page_name':'Education',
                           'sub_pages':vanamamalai_education.objects.values().count(),
                           'status':obj.filter(title__iexact = 'Education').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/vn_education_edit'
                        }
      data.append(education_data) 

      gallery_data = {
                           'id':obj.filter(title__iexact = 'Gallery').values_list('id',flat=True).last(),
                           'page_name':'Gallery',
                           'status':obj.filter(title__iexact = 'Gallery').values_list('show_status',flat=True).last(),
                           'page_link':'/admin/sub_admin_page/gallery_edit'
                        }
      data.append(gallery_data)

      res['all_page_data'] = data
      return Response(res)
   
   if request.method == 'PATCH':
      root_page_id = request.data['data']['root_page_id']
      page_status = request.data['data']['page_status']
      obj = rootPageStatus.objects.filter(id = root_page_id).values()
      if page_status == 'A':
         obj.update(show_status = False)
      if page_status == 'P':
         obj.update(show_status = True)
      res = {
               'status' : True,
               'message': 'root page show status updated successfully',
            }
      return Response(res)

@api_view(['GET','PUT'])
def home_page(request,format=None):
   if request.method == 'GET':
      obj = landing_page.objects.values()
      res = {}
      res['pageName'] = 'Home'
      mock_id = 1
      all_sections = []
      for i in obj:
         sub_dict = {}
         sub_dict['section_name'] = 'Section '+str(i['order'])
         sub_dict['section_id'] = i['id']
         sub_dict['status'] = i['show_status']
         section_data = [
                           {  'id':mock_id,
                              'title':'Heading',
                              'content':i['h1'],
                              'type':'text',
                              'link_status': True,
                           },
                           {
                              'id':mock_id+1,
                              'title':'Sub Heading',
                              'content':i['h2'],
                              'type':'text',
                              'link_status': False if i['layout'] in ['left_image','right_image'] else True

                           },
                           {
                              'id':mock_id+2,
                              'title':'Brief Info',
                              'content':i['p'],
                              'type':'text',
                              'link_status': True,
                           },
                           {
                              'id':mock_id+3,
                              'title':'Cover Image',
                              'content':i['img'].split('|'),
                              'type':'image',
                              'link_status': True,
                           },
                           {
                              'id':mock_id+4,
                              'title':'Background Color',
                              'content':i['background_color'],
                              'type':'color',
                              'link_status': False if i['layout'] in ['hero'] else True
                           },
                           {
                              'id':mock_id+5,
                              'title':'Youtube',
                              'content_title':i['yt_title'],
                              'content':i['yt_link'],
                              'type':'yt_link',
                              'link_status': True if i['layout'] in ['left_image','right_image'] else False
                           },
                           {
                              'id':mock_id+6,
                              'title':'PDF',
                              'content_title':i['file_title'],
                              'content':[i['file_link']],
                              'type':'file',
                              'link_status': True if i['layout'] in ['left_image','right_image'] else False
                           },
                           
                        ]
         mock_id = mock_id + 7
         sub_dict['section_data'] = section_data
         all_sections.append(sub_dict)
      
      res['all_sections'] = all_sections
      return Response(res)
   if request.method == 'PUT':
      data = request.data

      for i in data['all_sections']:
         obj = landing_page.objects.filter(id = i['section_id']).values().last()
         h1 = i['section_data'][0]['content']
         h2 = i['section_data'][1]['content']
         p = i['section_data'][2]['content']
         image = '|'.join(i['section_data'][3]['content'])
         background_color = i['section_data'][4]['content']
         yt_link = i['section_data'][5]['content']
         yt_title = i['section_data'][5]['content_title']
         file_link = i['section_data'][6]['content'][0]
         file_title =i['section_data'][6]['content_title']

         landing_page.objects.filter(id = i['section_id']).update(
                                                                     h1 = h1,
                                                                     h2 = h2,
                                                                     p = p,
                                                                     img = image,
                                                                     background_color = background_color,
                                                                     yt_link = yt_link,
                                                                     file_link = file_link,
                                                                     yt_title = yt_title,
                                                                     file_title = file_title,
                                                                  )
      res = {
               'status':True,
               'data':data
            }
      return Response()



@api_view(['POST','DELETE','PUT'])
def addSectionLandingPage(request,format=None):
   if request.method == 'POST':
      layout_type = request.data['layout_type']
      last_order = landing_page.objects.aggregate(max = Max('order'))['max']
      if layoutCreation(last_order,layout_type):
         res = {
                  'status': True,
                  'message':'new section created',
               }
      else:
         res = {
                  'status': False,
                  'message':'invalid layout type',
               }
      return Response(res)
   if request.method == 'DELETE':
      section_id = request.data['section_id']
      landing_page.objects.filter(id = section_id).delete()
      res = {
               'status':True,
               'message':'section deleted successfully'
            }
      return Response(res)
   if request.method == 'PUT':
      section_id = request.data['data']['section_id']
      current_status = request.data['data']['current_status']
      if current_status:
         landing_page.objects.filter(id = section_id).update(show_status = False)
      else:
         landing_page.objects.filter(id = section_id).update(show_status = True)

      res = {
               'status':True,
               'message':'section status changed successfully'
            }
      return Response(res)


@api_view(['GET','PUT','POST','DELETE','PATCH'])
def vn_temple_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method =="GET":
         obj = vanamamalai_temple.objects.filter(id = page_id).values().last()
         tab_obj = list(vanamamalai_temple_tab.objects.filter(temple_id = page_id)\
                                                .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['content_title']
         res['heading'] = obj['content_title']
         res['subheading'] = obj['content_subtitle']
         res['content_image'] = obj['content_image']
         
         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_id = data['page_id']
         heading = data['heading']
         subheading = data['subheading']
         content_image = data['content_image']
         vanamamalai_temple.objects.filter(id = page_id).update(
                                                                  content_title = heading,
                                                                  content_subtitle = subheading,
                                                                  content_image = content_image,
                                                               )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            vanamamalai_temple_tab.objects.filter(temple_id = page_id,id = tab_id)\
                                          .update(
                                                   tab_heading = tab_name,
                                                   tab_desc = tab_desc,
                                                   show_status = tab_show_status,
                                                 )
         res = {
                  'status':True,
                  'message':'Updation successfull'
         }
         return Response(res)
      
      if request.method == 'POST':
         page_id = request.data['page_id']
         
         data = vanamamalai_temple_tab(
                                    temple_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)

      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = vanamamalai_temple_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)

      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         vanamamalai_temple_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)

   else:
      if request.method == 'GET':
         obj = vanamamalai_temple.objects.values()
         res = {}
         res['pageName'] = obj.first()['banner_heading']
         mock_id = 1
         all_input_fields = [
                              {
                                 'content': obj.first()['banner_heading'],
                                 'id': mock_id,
                                 'title': "Heading",
                                 'type': "text",
                              },
                              {
                                 'content': obj.first()['banner_image'].split(','),
                                 'id': mock_id+1,
                                 'title': "Banner Image",
                                 'type': "image",
                                 },
                           ]
         res['all_input_fields'] = all_input_fields
         sub_page_list = obj.annotate(
                                          subpage_name = Lower(F('content_title')),
                                          subpage_link = Concat(
                                                                  V('/admin/sub_admin_page/vn_temple_edit/'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                               )
                                       )\
                           .values('id','subpage_name','subpage_link','show_status')
         res['sub_page_list'] = sub_page_list
         return Response(res)

      if request.method == 'PUT':
         data = request.data
         banner_heading = data['all_input_fields'][0]['content']
         banner_image = ''.join(data['all_input_fields'][1]['content'])
         vanamamalai_temple.objects.all().update(
                                                   banner_image = banner_image,
                                                   banner_heading = banner_heading,
                                                )
         res = {
                  'status':True,
                  'message':'Updation successfull',
               }
         return Response(res)

      if request.method == 'POST':
         data = vanamamalai_temple(
                                       banner_image = '',
                                       banner_heading = 'Vanamamalai Temple',
                                       content_title = 'New Section',
                                       content_subtitle = '', 
                                       content_image = '',
                                       show_status = False,
                                    )
         data.save()
         res = {
                  'status':True,
                  'message':'new section created successfully',
               }
         return Response(res)

      if request.method == 'DELETE':
         data = request.data
         vanamamalai_temple.objects.filter(id = data['id']).delete()
         vanamamalai_temple_tab.objects.filter(temple_id = data['id']).delete()
         res = {
               'status':True,
               'message':'deleted successfully',
            }
         return Response(data)

      if request.method == 'PATCH':
         data = request.data['data']
         obj = vanamamalai_temple.objects.filter(id = data['id']).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
               'status':True,
               'message':'status changed successfully',
            }
         return Response(res)      





@api_view(['GET','PUT','POST','DELETE','PATCH'])
def other_temple_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method =="GET":
         obj = vanamamalai_other_temple.objects.filter(id = page_id).values().last()
         tab_obj = list(vanamamalai_other_temple_tab.objects.filter(temple_id = page_id)\
                                                .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['content_title']
         res['heading'] = obj['content_title']
         res['subheading'] = obj['content_subtitle']
         res['content_image'] = obj['content_image']
         
         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_id = data['page_id']
         heading = data['heading']
         subheading = data['subheading']
         content_image = data['content_image']
         vanamamalai_other_temple.objects.filter(id = page_id).update(
                                                                  content_title = heading,
                                                                  content_subtitle = subheading,
                                                                  content_image = content_image,
                                                               )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            vanamamalai_other_temple_tab.objects.filter(temple_id = page_id,id = tab_id)\
                                          .update(
                                                   tab_heading = tab_name,
                                                   tab_desc = tab_desc,
                                                   show_status = tab_show_status,
                                                 )
         res = {
                  'status':True,
                  'message':'Updation successfull'
         }
         return Response(res)
      
      if request.method == 'POST':
         page_id = request.data['page_id']
         
         data = vanamamalai_other_temple_tab(
                                    temple_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)

      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = vanamamalai_other_temple_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)

      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         vanamamalai_other_temple_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)

   else:
      if request.method == 'GET':
         obj = vanamamalai_other_temple.objects.values()
         res = {}
         res['pageName'] = obj.first()['banner_heading']
         mock_id = 1
         all_input_fields = [
                              {
                                 'content': obj.first()['banner_heading'],
                                 'id': mock_id,
                                 'title': "Heading",
                                 'type': "text",
                              },
                              {
                                 'content': obj.first()['banner_image'].split(','),
                                 'id': mock_id+1,
                                 'title': "Banner Image",
                                 'type': "image",
                                 },
                           ]
         res['all_input_fields'] = all_input_fields
         sub_page_list = obj.annotate(
                                          subpage_name = Lower(F('content_title')),
                                          subpage_link = Concat(
                                                                  V('/admin/sub_admin_page/other_temple_edit/'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                               )
                                       )\
                           .values('id','subpage_name','subpage_link','show_status')
         res['sub_page_list'] = sub_page_list
         return Response(res)

      if request.method == 'PUT':
         data = request.data
         banner_heading = data['all_input_fields'][0]['content']
         banner_image = ''.join(data['all_input_fields'][1]['content'])
         vanamamalai_other_temple.objects.all().update(
                                                   banner_image = banner_image,
                                                   banner_heading = banner_heading,
                                                )
         res = {
                  'status':True,
                  'message':'Updation successfull',
               }
         return Response(res)

      if request.method == 'POST':
         obj = vanamamalai_other_temple.objects.values().first()
         data = vanamamalai_other_temple(
                                       banner_image = obj['banner_image'],
                                       banner_heading = obj['banner_heading'],
                                       content_title = 'New Section',
                                       content_subtitle = '', 
                                       content_image = '',
                                       show_status = False,
                                    )
         data.save()
         res = {
                  'status':True,
                  'message':'new section created successfully',
               }
         return Response(res)

      if request.method == 'DELETE':
         data = request.data
         vanamamalai_other_temple.objects.filter(id = data['id']).delete()
         vanamamalai_other_temple_tab.objects.filter(temple_id = data['id']).delete()
         res = {
               'status':True,
               'message':'deleted successfully',
            }
         return Response(data)

      if request.method == 'PATCH':
         data = request.data['data']
         obj = vanamamalai_other_temple.objects.filter(id = data['id']).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
               'status':True,
               'message':'status changed successfully',
            }
         return Response(res)      







@api_view(['GET','PUT','POST','DELETE','PATCH'])
def branches_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method =="GET":
         obj = vanamamalai_mutt_branches.objects.filter(id = page_id).values().last()
         tab_obj = list(vanamamalai_mutt_branches_tab.objects.filter(branch_id = page_id)\
                                                .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['content_title']
         res['heading'] = obj['content_title']
         res['subheading'] = obj['content_subtitle']
         res['content_image'] = obj['content_image']
         
         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_id = data['page_id']
         heading = data['heading']
         subheading = data['subheading']
         content_image = data['content_image']
         vanamamalai_mutt_branches.objects.filter(id = page_id).update(
                                                                  content_title = heading,
                                                                  content_subtitle = subheading,
                                                                  content_image = content_image,
                                                               )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            vanamamalai_mutt_branches_tab.objects.filter(branch_id = page_id,id = tab_id)\
                                          .update(
                                                   tab_heading = tab_name,
                                                   tab_desc = tab_desc,
                                                   show_status = tab_show_status,
                                                 )
         res = {
                  'status':True,
                  'message':'Updation successfull'
         }
         return Response(res)
      
      if request.method == 'POST':
         page_id = request.data['page_id']
         
         data = vanamamalai_mutt_branches_tab(
                                    branch_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)

      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = vanamamalai_mutt_branches_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)

      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         vanamamalai_mutt_branches_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)

   else:
      if request.method == 'GET':
         obj = vanamamalai_mutt_branches.objects.values()
         res = {}
         res['pageName'] = obj.first()['banner_heading']
         mock_id = 1
         all_input_fields = [
                              {
                                 'content': obj.first()['banner_heading'],
                                 'id': mock_id,
                                 'title': "Heading",
                                 'type': "text",
                              },
                              {
                                 'content': obj.first()['banner_image'].split(','),
                                 'id': mock_id+1,
                                 'title': "Banner Image",
                                 'type': "image",
                                 },
                           ]
         res['all_input_fields'] = all_input_fields
         sub_page_list = obj.annotate(
                                          subpage_name = Lower(F('content_title')),
                                          subpage_link = Concat(
                                                                  V('/admin/sub_admin_page/branches_edit/'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                               )
                                       )\
                           .values('id','subpage_name','subpage_link','show_status')
         res['sub_page_list'] = sub_page_list
         return Response(res)

      if request.method == 'PUT':
         data = request.data
         banner_heading = data['all_input_fields'][0]['content']
         banner_image = ''.join(data['all_input_fields'][1]['content'])
         vanamamalai_mutt_branches.objects.all().update(
                                                   banner_image = banner_image,
                                                   banner_heading = banner_heading,
                                                )
         res = {
                  'status':True,
                  'message':'Updation successfull',
               }
         return Response(res)

      if request.method == 'POST':
         obj = vanamamalai_mutt_branches.objects.values().first()
         data = vanamamalai_mutt_branches(
                                       banner_image = obj['banner_image'],
                                       banner_heading = obj['banner_heading'],
                                       content_title = 'New Section',
                                       content_subtitle = '', 
                                       content_image = '',
                                       show_status = False,
                                    )
         data.save()
         res = {
                  'status':True,
                  'message':'new section created successfully',
               }
         return Response(res)

      if request.method == 'DELETE':
         data = request.data
         vanamamalai_mutt_branches.objects.filter(id = data['id']).delete()
         vanamamalai_mutt_branches_tab.objects.filter(branch_id = data['id']).delete()
         res = {
               'status':True,
               'message':'deleted successfully',
            }
         return Response(data)

      if request.method == 'PATCH':
         data = request.data['data']
         obj = vanamamalai_mutt_branches.objects.filter(id = data['id']).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
               'status':True,
               'message':'status changed successfully',
            }
         return Response(res)




@api_view(['GET','PUT','POST','DELETE','PATCH'])
def vn_education_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method =="GET":
         obj = vanamamalai_education.objects.filter(id = page_id).values().last()
         tab_obj = list(vanamamalai_education_tab.objects.filter(education_id = page_id)\
                                                .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['content_title']
         res['heading'] = obj['content_title']
         res['subheading'] = obj['content_subtitle']
         res['content_image'] = obj['content_image']
         
         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_id = data['page_id']
         heading = data['heading']
         subheading = data['subheading']
         content_image = data['content_image']
         vanamamalai_education.objects.filter(id = page_id).update(
                                                                  content_title = heading,
                                                                  content_subtitle = subheading,
                                                                  content_image = content_image,
                                                               )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            vanamamalai_education_tab.objects.filter(education_id = page_id,id = tab_id)\
                                          .update(
                                                   tab_heading = tab_name,
                                                   tab_desc = tab_desc,
                                                   show_status = tab_show_status,
                                                 )
         res = {
                  'status':True,
                  'message':'Updation successfull'
         }
         return Response(res)
      
      if request.method == 'POST':
         page_id = request.data['page_id']
         
         data = vanamamalai_education_tab(
                                    education_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)

      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = vanamamalai_education_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)

      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         vanamamalai_education_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)

   else:
      if request.method == 'GET':
         obj = vanamamalai_education.objects.values()
         res = {}
         res['pageName'] = obj.first()['banner_heading']
         mock_id = 1
         all_input_fields = [
                              {
                                 'content': obj.first()['banner_heading'],
                                 'id': mock_id,
                                 'title': "Heading",
                                 'type': "text",
                              },
                              {
                                 'content': obj.first()['banner_image'].split(','),
                                 'id': mock_id+1,
                                 'title': "Banner Image",
                                 'type': "image",
                                 },
                           ]
         res['all_input_fields'] = all_input_fields
         sub_page_list = obj.annotate(
                                          subpage_name = Lower(F('content_title')),
                                          subpage_link = Concat(
                                                                  V('/admin/sub_admin_page/branches_edit/'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                               )
                                       )\
                           .values('id','subpage_name','subpage_link','show_status')
         res['sub_page_list'] = sub_page_list
         return Response(res)

      if request.method == 'PUT':
         data = request.data
         banner_heading = data['all_input_fields'][0]['content']
         banner_image = ''.join(data['all_input_fields'][1]['content'])
         vanamamalai_education.objects.all().update(
                                                   banner_image = banner_image,
                                                   banner_heading = banner_heading,
                                                )
         res = {
                  'status':True,
                  'message':'Updation successfull',
               }
         return Response(res)

      if request.method == 'POST':
         obj = vanamamalai_education.objects.values().first()
         data = vanamamalai_education(
                                       banner_image = obj['banner_image'],
                                       banner_heading = obj['banner_heading'],
                                       content_title = 'New Section',
                                       content_subtitle = '', 
                                       content_image = '',
                                       show_status = False,
                                    )
         data.save()
         res = {
                  'status':True,
                  'message':'new section created successfully',
               }
         return Response(res)

      if request.method == 'DELETE':
         data = request.data
         vanamamalai_education.objects.filter(id = data['id']).delete()
         vanamamalai_education_tab.objects.filter(education_id = data['id']).delete()
         res = {
               'status':True,
               'message':'deleted successfully',
            }
         return Response(data)

      if request.method == 'PATCH':
         data = request.data['data']
         obj = vanamamalai_education.objects.filter(id = data['id']).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
               'status':True,
               'message':'status changed successfully',
            }
         return Response(res)



@api_view(['GET','PUT','POST','DELETE','PATCH'])
def ponnadikkal_jeeyar_edit(request,format=None):
      page_id = request.GET.get('page_id')
      if request.method =="GET":
         obj = ponnadikkal_jeeyar.objects.filter(id = page_id).values().last()
         tab_obj = list(ponnadikkal_jeeyar_tab.objects.filter(jeeyar_id = page_id)\
                                                .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['content_title']
         res['heading'] = obj['content_title']
         res['subheading'] = obj['content_subtitle']
         res['content_image'] = obj['content_image']
         res['banner_image'] = obj['banner_image']
         
         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_id = data['page_id']
         heading = data['heading']
         subheading = data['subheading']
         content_image = data['content_image']
         banner_image = data['banner_image']
         ponnadikkal_jeeyar.objects.filter(id = page_id).update(
                                                                  content_title = heading,
                                                                  content_subtitle = subheading,
                                                                  content_image = content_image,
                                                                  banner_image = banner_image,
                                                               )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            ponnadikkal_jeeyar_tab.objects.filter(jeeyar_id = page_id,id = tab_id)\
                                          .update(
                                                   tab_heading = tab_name,
                                                   tab_desc = tab_desc,
                                                   show_status = tab_show_status,
                                                 )
         res = {
                  'status':True,
                  'message':'Updation successfull'
         }
         return Response(res)
      
      if request.method == 'POST':
         page_id = request.data['page_id']
         
         data = ponnadikkal_jeeyar_tab(
                                    jeeyar_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)

      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = ponnadikkal_jeeyar_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)

      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         ponnadikkal_jeeyar_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)




@api_view(['GET','PUT','POST','PATCH','DELETE'])
def jeeyars_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method == 'GET':
         obj = jeeyars.objects.filter(id = page_id).values().last()
         tab_obj = list(jeeyars_tab.objects.filter(jeeyar_id = page_id)\
                                      .annotate(
                                                            tab_name = F('tab_heading'),
                                                            tab_id = F('id'),
                                                            tab_data = F('tab_desc')
                                                ).values('tab_name','tab_id','tab_data','show_status'))
         res = {}
         res['page_id'] = page_id
         res['pageName'] = obj['banner_heading']
         res['subPageName'] = obj['name']
         res['content_image'] = obj['image']

         c = 1
         for i in tab_obj:
            i['tab_data'] = eval(i['tab_data'])
            for j in i['tab_data']:
               j['id'] = 'bf'+str(c)
               c = c + 1
         res['all_tabs'] = tab_obj
         res['new_id'] = c   
         return Response(res)
      
      if request.method  == 'PUT':
         data = request.data
         page_id = data['page_id']
         content_image = data['content_image']
         
         jeeyars.objects.filter(id = page_id).update(
                                                      image = content_image,
                                                    )
         for i in data['all_tabs']:
            tab_show_status = i['show_status']
            tab_name = i['tab_name']
            tab_id = i['tab_id']
            tab_desc = str(i['tab_data'])
            jeeyars_tab.objects.filter(jeeyar_id = page_id,id = tab_id)\
                               .update( 
                                          tab_heading = tab_name,
                                          tab_desc = tab_desc,
                                          show_status = tab_show_status,
                                       )
         res = {
                  'status':True,
                  'message':'Updation successfull'
               }
         return Response(res)

      if request.method == 'POST':
         page_id = request.data['page_id']
         data = jeeyars_tab(
                                    jeeyar_id = page_id,
                                    tab_heading = 'New Tab',
                                    tab_desc = "[{'data': 'Lorem ipsum', 'type': 'text'}]",
                                    show_status = False,
                               )
         data.save()
         res = {
                  'status': True,
                  'message': 'new tab created successfully'
               }
         return Response(res)
      
      if request.method == 'PATCH':
         tab_id = request.data['data']['tab_id']
         obj = jeeyars_tab.objects.filter(id = tab_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'tab show status updated successfully',
               }
         return Response(res)
      
      if request.method == "DELETE":
         tab_id = request.data['tab_id']
         jeeyars_tab.objects.filter(id = tab_id).delete()
         res = {
                  'status':True,
                  'message':' tab deleted successfully',
               }
         return Response(res)


   else:
      if request.method == 'GET':
         res = {}
         obj = jeeyars.objects.values()
         res['pageName'] = obj.first()['banner_heading']
         res['banner_image'] = obj.first()['banner_image']
         jeeyar_list = obj.annotate(
                                       sub_page_link = Concat(
                                                              V('/admin/sub_admin_page/jeeyars_edit/'),
                                                              Cast('id',CharField()),
                                                              output_field=CharField()
                                                            )
                                   )\
                           .values('id',
                                  'name',
                                  'image',
                                  'jeeyar_no',
                                  'start_date',
                                  'end_date',
                                  'prefix',
                                  'show_status',
                                  'sub_page_link',
                                  )
         res['jeeyar_list'] = jeeyar_list
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         page_name = data['pageName']
         banner_image = data['banner_image']
         jeeyars.objects.update(
                                 banner_heading = page_name,
                                 banner_image = banner_image,
                               )

         def ordinaltg(n):
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")


         for i in data['jeeyar_list']:
            obj = jeeyars.objects.filter(id = i['id'])
            obj.update(
                        name = i['name'],
                        image = i['image'],
                        jeeyar_no = i['jeeyar_no'],
                        start_date = i['start_date'],
                        end_date = i['end_date'],
                        prefix = i['prefix'],
                        show_status = i['show_status'],
                        jeeyar_no_suffix = '' if i['jeeyar_no'] == None else ordinaltg(int(i['jeeyar_no']))
                      )
         res = {
                  'status':True,
                  'message':'Updation successfull',
               }
         return Response(res)
      
      if request.method == 'POST':
         data = jeeyars(
                           name = 'New Jeeyar',
                           show_status = False,
                       )
         data.save()
         res = {
                  'status':True,
                  'message': 'new jeeyar created successfully'
               }
         return Response(res)

      if request.method == "PATCH":
         jeeyar_id = request.data['data']['jeeyar_id']
         obj = jeeyars.objects.filter(id = jeeyar_id).values()
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'jeeyar show status updated successfully',
               }
         return Response(res)
      
      if request.method == 'DELETE':
         jeeyar_id = request.data['jeeyar_id']
         jeeyars.objects.filter(id = jeeyar_id).delete()
         jeeyars_tab.objects.filter(jeeyar_id = jeeyar_id).delete()
         res = {
                  'status' : True,
                  'message': 'jeeyar deleted successfully',
               }
         return Response(res)
      

@api_view(['GET','PUT','POST','PATCH','DELETE'])
def gallery_edit(request,format=None):
   page_id = request.GET.get('page_id')
   if page_id != None:
      if request.method == 'GET':
         obj = gallery_album.objects.filter(id = page_id).values().last()
         res = {}
         res['page_id'] = page_id
         res['album_name'] = obj['album_name']
         
         content_array = gallery.objects.filter(album_id = obj['id']).values('id','image','name','details')
         res['content_array'] = content_array
         return Response(res)
   
      if request.method == 'PUT':
         data = request.data
         print(data)
         page_id = data['page_id']
         album_name = data['album_name']
         gallery_album.objects.filter(id = page_id).update(album_name = album_name)

         for i in data['content_array']:
            gallery.objects.filter(id = i['id']).update(
                                                         name = i['name'],
                                                         image = i['image'],
                                                         details = i['details']
                                                      )
         res = {
                  'status':True,
                  'message':'updation successfull'
               }
         

         return Response(res)
      
      if request.method == 'POST':
         data = request.data
         album_id = data['page_id']
         data = gallery(
                           album_id = album_id
                       )
         data.save()

         res = {
                  'status':True,
                  'message':'new album content created successfully'
               }
         return Response(res)
      
      if request.method == 'DELETE':
         data = request.data
         gallery.objects.filter(id = data['image_id'],album_id = data['album_id']).delete()
         res = {
                  'status':True,
                  'message':'Image deleted successfull'
               }
         return Response(res)



   
   else:
      if request.method == 'GET':
         gallery_head = gallery_details.objects.values().last()
         res = {}
         res['pageName'] = gallery_head['banner_heading']
         res['banner_image'] = gallery_head['banner_image']

         yt_links = gallery_youtube.objects.values()
         res['yt_links'] = yt_links

         albums = gallery_album.objects\
                               .annotate(
                                           album_link = Concat(
                                                                  V('/admin/sub_admin_page/gallery_edit/'),
                                                                  Cast('id',CharField()),
                                                                  output_field=CharField()
                                                               )
                                        )\
                               .values()
         res['albums'] = albums
         return Response(res)
      
      if request.method == 'PUT':
         data = request.data
         banner_heading = data['pageName']
         banner_image = data['banner_image']
         gallery_details.objects.update( banner_heading = banner_heading,banner_image = banner_image)

         for i in data['yt_links']:
            gallery_youtube.objects.filter(id = i['id'])\
                                   .update(
                                             title = i['title'],
                                             url = i['url'],
                                          )
         
         for i in data['albums']:
            gallery_album.objects.filter(id = i['id']).update(album_name = i['album_name'])
         
         res = {
                  'status':True,
                  'message':'updation successfull'
               }
         

         return Response(res)

      if request.method == 'POST':
         if request.data['type'] == 'y':
            data = gallery_youtube(
                                       title = 'new title', 
                                       url = 'new link',
                                  )
            data.save()
            res = {
                  'status':True,
                  'message':'new youtube link created successfull'
               }
            return Response(res)
         if request.data['type'] == 'a':
            data = gallery_album(
                                       album_name = 'new album', 
                                       show_status = False,
                                  )
            data.save()
            res = {
                  'status':True,
                  'message':'new youtube link created successfull'
               }
            return Response(res)

      if request.method == 'PATCH':
         album_id = request.data['data']['album_id']
         obj = gallery_album.objects.filter(id = album_id).values()
         
         if obj.last()['show_status']:
            obj.update(show_status = False)
         else:
            obj.update(show_status = True)
         res = {
                  'status' : True,
                  'message': 'album show status updated successfully',
               }
         return Response(res)
      
      if request.method == 'DELETE':
         if request.data['type'] == 'y':
            yt_id = request.data['id']
            gallery_youtube.objects.filter(id = yt_id).delete()
            res = {
                  'status':True,
                  'message':'youtube link deleted successfull'
               }
            return Response(res)
         if request.data['type'] == 'a':
            album_id = request.data['id']
            gallery_album.objects.filter(id = album_id).delete()
            gallery.objects.filter(album_id = album_id).delete()
            res = {
                  'status':True,
                  'message':'album deleted successfull'
               }
            return Response(res)
         



@api_view(['POST'])
def adminAddNewTabData(request,format=None):
   id = int(request.data['id']) + 1
   type1 =request.data['type']
   array = eval(request.data['dataArray'])[0]
   tab_id = eval(request.data['tabId'])[0]

   page_data = request.data['pageData'].replace('true','True')
   page_data = page_data.replace('false','False')
   page_data = eval(page_data)
   
   res = addTab(id,type1,array)
   for i in page_data['all_tabs']:
      if i['tab_id'] == tab_id:
         i['tab_data'] = res
         break
   page_data['new_id'] = int(page_data['new_id'])+1
   return Response(page_data)


@api_view(['POST'])
def addImageTabDataAdmin(request,format=None):
   file = request.FILES['file']
   id = int(request.data['id'])+1
   array = eval(request.data['dataArray'])[0]
   tab_id = eval(request.data['tabId'])[0]

   page_data = request.data['pageData'].replace('true','True')
   page_data = page_data.replace('false','False')
   page_data = eval(page_data)
   
   img_path = 'img/'
   upload_res = image_upload(file,img_path)
   updated_value = 'media/'+upload_res
   array.append({
                  'data':updated_value,
                  'type':'image',
                  'id':'bf'+str(id)

               })
   for i in page_data['all_tabs']:
      if i['tab_id'] == tab_id:
         i['tab_data'] = array
         break
   page_data['new_id'] = int(page_data['new_id'])+1
   
   return Response(page_data)



@api_view(['POST'])
def addImageJeeyarAdmin(request,format=None):
   file = request.FILES['file']
   id = int(request.data['id'])
   page_data = request.data['pageData'].replace('true','True')
   page_data = page_data.replace('false','False')
   page_data = eval(page_data)

   img_path = 'img/'
   upload_res = image_upload(file,img_path)
   updated_value = 'media/'+upload_res

   for i in page_data['jeeyar_list']:
      if i['id']  == id:
         i['image'] = updated_value
         break
   return Response(page_data)
