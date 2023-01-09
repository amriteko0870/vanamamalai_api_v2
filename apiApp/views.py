import pandas as pd
from datetime import datetime as dt
from operator import itemgetter 
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

#----------------------------models---------------------------------------------------
from apiApp.models import landing_page,vanamamalai_temple,vanamamalai_temple_tab
from apiApp.models import gallery,gallery_album,gallery_details,gallery_youtube
from apiApp.models import jeeyars,jeeyars_tab
from apiApp.models import vanamamalai_other_temple,vanamamalai_other_temple_tab
from apiApp.models import vanamamalai_mutt_branches,vanamamalai_mutt_branches_tab
from apiApp.models import ponnadikkal_jeeyar,ponnadikkal_jeeyar_tab
from apiApp.models import vanamamalai_education,vanamamalai_education_tab

#-----------------------------extra -----------------------------------------------------
from apiApp.extra import sample_gallery
from apiApp.admin_pages.image_upload import image_upload

@api_view(['GET'])
def landingPage(request,format=None):
    data = landing_page.objects.filter(show_status = True).annotate(
                                        seq_no = Concat(V('landing_page_'),Cast('order',CharField()),output_field=CharField()),
                                        ).values()
    n_data = pd.DataFrame(data)
    n_data['img'] = n_data['img'].str.split('|')
    res = n_data.to_dict(orient='records')
    for i in res:
        while '' in i['img']:
            i['img'].remove('')
    gallery = sample_gallery()
    res.insert(2,gallery)
    return Response({
                    'message':'True',
                    'data':res
                   })



@api_view(['POST'])
def vn_temple(request,format=None):
    id = request.data['id']
    res = {}
    obj = vanamamalai_temple.objects.filter(id = id).values().last()
    tab = vanamamalai_temple_tab.objects.filter(temple_id = id,show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    content = {
                'title': obj['content_title'],
                'sub_title': obj['content_subtitle'] ,
                'image': obj['content_image'],
              }
    res['content'] = content
    tab_data = []
    jsonDec = json.decoder.JSONDecoder()
    for i in tab:
        tab_content = {}
        tab_content['name'] = i['tab_heading']
        tab_content['content'] = eval(i['tab_desc'])
        # tab_content['content'] = jsonDec.decode(i['tab_desc'])

        tab_data.append(tab_content)

    res['tab_data'] = tab_data
    return Response(res)


@api_view(['GET'])
def gallery_page(request,format=None):
    res = {}

    obj = gallery_details.objects.values().last()
    banner = {
                "heading": obj['banner_heading'],
                'image': obj['banner_image'] 
             }
    res['banner'] = banner

    obj = gallery_youtube.objects.annotate(
                                            video_title = F('title'),
                                            video_id = F('url')
                                          ).values('video_title','video_id')
    res['carousel_data'] = obj

    content = []
    albums = gallery_album.objects.filter(show_status = True).values_list('album_name','id')
    for i in albums:
        d = {
              'title' : i[0],
              'id':i[1]
            }
        content_data = gallery.objects.filter(album_id = i[1]).values('name','image','details')
        d['content_data'] = content_data

        content.append(d)
    res['content'] = content

    return Response(res)
    
# @api_view(['POST'])
# def sub_album_page(request,format=None):
#     sub_album_name = request.data['sub_album_name']
#     album_id  = request.data['album_id']
#     album_name = gallery_album.objects.filter(id = album_id).values().last()['album_name']
#     res = {}

#     obj = gallery_details.objects.values().last()
#     banner = {
#                 "heading": obj['banner_heading'],
#                 'image': obj['banner_image'] 
#              }
#     res['banner'] = banner

#     obj = gallery_sub_album.objects.filter(sub_album_name = sub_album_name,album_name = album_name).values().last()

#     res['title'] = obj['sub_album_name']
    
#     album_banner = {
#                     'p': obj['sub_album_details'],
#                     'image': obj['sub_album_image']
#                    }
#     res['album_banner'] = album_banner

#     content = gallery.objects.filter(sub_album_name = sub_album_name,album_name = album_name)\
#                              .annotate(
#                                         sub_heading = F('name'),
#                              ).values('sub_heading','image','details')
#     res['content'] = content
#     return Response(res)

# @api_view(['POST'])
# def all_sub_album_page(request,format=None):
#     album_id  = request.data['album_id']
#     album_name = gallery_album.objects.filter(id = album_id).values().last()['album_name']
#     res = {}

#     obj = gallery_details.objects.values().last()
#     banner = {
#                 "heading": obj['banner_heading'],
#                 'image': obj['banner_image'] 
#              }
#     res['banner'] = banner

#     res['title'] = album_name

#     res['id'] = album_id

#     content = gallery_sub_album.objects.filter(album_name = album_name)\
#                                        .annotate(
#                                                  sub_heading = F('sub_album_name'),
#                                                  image = F('sub_album_image')
#                                                 ).values('sub_heading','image')

#     res['content'] = content

#     return Response(res)


@api_view(['GET'])
def jeeyars_parampara(request,format=None):
    res = {}
    res['title'] = "Jeeyar Paramapara"
    res['call_link'] = "jeeyars_details"
    jeeyar = jeeyars.objects.filter(show_status = True).values('id','image','name','prefix','start_date','end_date','jeeyar_no','jeeyar_no_suffix')
    res['jeeyars'] = jeeyar
    return Response(res)

@api_view(['POST'])
def jeeyars_details(request,format=None):
    id = request.data['id']
    res = {}
    obj = jeeyars.objects.filter(id = id).values().last()
    tab = jeeyars_tab.objects.filter(jeeyar_id = id,show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    sub_title = obj['start_date']+" "+" to "+obj['end_date']+" "+obj['prefix']  if obj['end_date'] != "" else obj['start_date']+" "+obj['prefix']
    content = {
                'title': obj['name'],
                'sub_title': sub_title ,
                'image': obj['image'],
                'jeeyar_no':str(obj['jeeyar_no'])+obj['jeeyar_no_suffix']
              }
    res['content'] = content
    if len(tab) > 0:
        tab_data = []
        for i in tab:
            tab_content = {}
            tab_content['name'] = i['tab_heading']
            tab_content['content'] = eval(i['tab_desc'])

            tab_data.append(tab_content)
    else:
        tab_data = [
                        {
                        "name": "About",
                        "content": [
                            {
                            "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
                            "type": "text"
                            }
                        ]
                        },
                        {
                        "name": "Place",
                        "content": [
                            {
                            "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. e ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
                            "type": "text"
                            }
                        ]
                        },
                        {
                        "name": "AchAryan/Sishya",
                        "content": [
                            {
                            "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
                            "type": "text"
                            }
                        ]
                        },
                        {
                        "name": "Works",
                        "content": [
                            {
                            "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit",
                            "type": "text"
                            }
                        ]
                        }
                    ]

    res['tab_data'] = tab_data

    return Response(res)

@api_view(['POST'])
def other_temple(request,format=None):
    id = request.data['id']
    res = {}
    obj = vanamamalai_other_temple.objects.filter(id = id).values().last()
    tab = vanamamalai_other_temple_tab.objects.filter(temple_id = id,show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    content = {
                'title': obj['content_title'],
                'sub_title': obj['content_subtitle'] ,
                'image': obj['content_image'],
              }
    res['content'] = content
    
    tab_data = []
    for i in tab:
        tab_content = {}
        tab_content['name'] = i['tab_heading']
        tab_content['content'] = eval(i['tab_desc'])

        tab_data.append(tab_content)

    res['tab_data'] = tab_data
    return Response(res)

@api_view(['POST'])
def branches(request,format=None):
    id = request.data['id']
    res = {}
    obj = vanamamalai_mutt_branches.objects.filter(id = id).values().last()
    tab = vanamamalai_mutt_branches_tab.objects.filter(branch_id = id,show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    content = {
                'title': obj['content_title'],
                'sub_title': obj['content_subtitle'] ,
                'image': obj['content_image'],
              }
    res['content'] = content
    
    tab_data = []
    for i in tab:
        tab_content = {}
        tab_content['name'] = i['tab_heading']
        tab_content['content'] = eval(i['tab_desc'])

        tab_data.append(tab_content)

    res['tab_data'] = tab_data
    return Response(res)


@api_view(['POST'])
def vn_education(request,format=None):
    id = request.data['id']
    res = {}
    obj = vanamamalai_education.objects.filter(id = id).values().last()
    tab = vanamamalai_education_tab.objects.filter(education_id = id,show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    content = {
                'title': obj['content_title'],
                'sub_title': obj['content_subtitle'] ,
                'image': obj['content_image'],
              }
    res['content'] = content
    
    tab_data = []
    for i in tab:
        tab_content = {}
        tab_content['name'] = i['tab_heading']
        tab_content['content'] = eval(i['tab_desc'])

        tab_data.append(tab_content)

    res['tab_data'] = tab_data
    return Response(res)

@api_view(['POST'])
def ponnadikkal_jeeyars(request,format=None):
    res = {}
    obj = ponnadikkal_jeeyar.objects.values().last()
    tab = ponnadikkal_jeeyar_tab.objects.filter(show_status = True).values()

    banner = {
                'heading': obj['banner_heading'],
                'image': obj['banner_image'],
             }
    res['banner'] = banner

    content = {
                'title': obj['content_title'],
                'sub_title': obj['content_subtitle'] ,
                'image': obj['content_image'],
              }
    res['content'] = content
    
    tab_data = []
    for i in tab:
        tab_content = {}
        tab_content['name'] = i['tab_heading']
        tab_content['content'] = eval(i['tab_desc'])

        tab_data.append(tab_content)

    res['tab_data'] = tab_data
    return Response(res)



@api_view(['POST'])
def newImageUpload(request,format=None):
    file = request.FILES['file']
    index = request.data['index']
    imageArray = request.data['image_array'].split(',')
    img_path = 'img/'
    upload_res = image_upload(file,img_path)
    updated_value = 'media/'+upload_res
    imageArray[int(index)] = updated_value
    return Response({'image_array':imageArray})


@api_view(['GET'])
def fileDownload(request,format=None):
    file_name =  request.GET.get('file_name')
    response = FileResponse(open(file_name, 'rb'))
    return response


# @api_view(['GET'])
# def index(request):
#     j = [
#         {
#             "id": 1,
#             "image": "media/img/jeeyars/sample.svg",
#             "name": "Shri Ramanuja alias Sri Udayavar",
#             "prefix": "AD",
#             "start_date": "1017",
#             "end_date": "",
#             "jeeyar_no": 1,
#             "jeeyar_no_suffix": "st"
#         },
#         {
#             "id": 2,
#             "image": "media/img/jeeyars/sample.svg",
#             "name": "Shri Manavala Maamunigal",
#             "prefix": "AD",
#             "start_date": "1370",
#             "end_date": "",
#             "jeeyar_no": 2,
#             "jeeyar_no_suffix": "nd"
#         },
#         {
#             "id": 3,
#             "image": "media/img/jeeyars/sample.svg",
#             "name": "Ponnadikkal Jeeyar",
#             "prefix": "AD",
#             "start_date": "1447",
#             "end_date": "1482",
#             "jeeyar_no": 3,
#             "jeeyar_no_suffix": "rd"
#         },
#         {
#             "id": 4,
#             "image": "media/img/jeeyars/sample.svg",
#             "name": "Sri Chendalangara Ramanuja Jeer Swami",
#             "prefix": "AD",
#             "start_date": "1502",
#             "end_date": "1520",
#             "jeeyar_no": 4,
#             "jeeyar_no_suffix": "th"
#         },
#         {
#             "id": 5,
#             "image": "media/img/jeeyars/sample.svg",
#             "name": "Sri Rengappa Ramanuja Swami",
#             "prefix": "AD",
#             "start_date": "1520",
#             "end_date": "1586",
#             "jeeyar_no": 5,
#             "jeeyar_no_suffix": "th"
#         }
#     ]
#     a = [
#         {
#             "name": "About",
#             "content": [
#                 {
#                     "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
#                     "type": "text"
#                 }
#             ]
#         },
#         {
#             "name": "Place",
#             "content": [
#                 {
#                     "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. e ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
#                     "type": "text"
#                 }
#             ]
#         },
#         {
#             "name": "AchAryan/Sishya",
#             "content": [
#                 {
#                     "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
#                     "type": "text"
#                 }
#             ]
#         },
#         {
#             "name": "Works",
#             "content": [
#                 {
#                     "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit",
#                     "type": "text"
#                 }
#             ]
#         }
#     ]

#     jeeyars.objects.all().delete()
#     jeeyars_tab.objects.all().delete()
#     for i in j:
#         data = jeeyars(
#                         name = i['name'],
#                         prefix = i['prefix'],
#                         start_date = i['start_date'],
#                         end_date = i['end_date'],
#                         jeeyar_no_suffix = i['jeeyar_no_suffix'],
#                         image = i['image'],
#                         jeeyar_no = i['jeeyar_no']
#                        )
#         data.save()
#         for k in a :
#             name = k['name']
#             content = k['content']
#             json_content = json.dumps(content)
#             data1 = jeeyars_tab(
#                                     jeeyar_id = data.id,
#                                     tab_heading = name,
#                                     tab_desc = json_content,
#                                 )
#             data1.save()

#     return Response('sample')

@api_view(['GET'])
def index(format=None):
    # # vanamamalai_education.objects.all().delete()
    # # vanamamalai_temple_tab.objects.all().delete()
    # banner_image = 'media/img/vanamamalai_temple/banner.png'
    # banner_heading = 'Education'
    # content_title = 'Sri Vanachala Vidhya Peetam' #Mela Thiruvengadamudyaan
    # content_subtitle = 'Lorem Ipsum'
    # content_image = 'media/img/vanamamalai_temple/10.png'

    # data = vanamamalai_education(
    #                     banner_image = banner_image,
    #                     banner_heading = banner_heading,
    #                     content_title = content_title,
    #                     content_subtitle = content_subtitle,
    #                     content_image = content_image,
    # )
    # data.save()
    # print('################  id : ',data.id)
    # a = [
    #     {
    #         "name": "About",
    #         "content": [
    #             {
    #                 "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
    #                 "type": "text"
    #             }
    #         ]
    #     },
    #     {
    #         "name": "Admission",
    #         "content": [
    #             {
    #                 "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. e ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
    #                 "type": "text"
    #             }
    #         ]
    #     },
    #     {
    #         "name": "Curriculum",
    #         "content": [
    #             {
    #                 "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium.",
    #                 "type": "text"
    #             }
    #         ]
    #     },
    #     {
    #         "name": "Faculties",
    #         "content": [
    #             {
    #                 "data": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit quasi illo praesentium. Sit nam non distinctio exercitationem, quaerat reiciendis illo molestias. Deleniti ipsum odit cum laudantium. Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet quo ipsam accusantium molestias nobis perspiciatis sapiente ipsa eveniet dolore cupiditate at adipisci non omnis expedita, qui error repudiandae magnam enim quisquam tempora reprehenderit",
    #                 "type": "text"
    #             }
    #         ]
    #     }
    # ]
    # for i in a:
    #     name = i['name']
    #     content = i['content']
    #     json_content = json.dumps(content)
    #     data1 = vanamamalai_education_tab(
    #                             education_id = data.id,
    #                             tab_heading = name,
    #                             tab_desc = json_content,
    #                           )
    #     data1.save()
    return Response('sample')




