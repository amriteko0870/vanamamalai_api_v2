
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

import apiApp.views as views
import apiApp.user_views as u_views
import apiApp.sidebar_views as s_views
import apiApp.admin_pages.admin_views as admin_views

urlpatterns = [
    #-------------------Filters------------------------------------
    path('sideBar',s_views.sideBar,name='sideBar'),
    path('sideBarAdmin',s_views.sideBarAdmin,name='sideBarAdmin'),


    path('landingPage',views.landingPage,name='landingPage'),
    path('vn_temple',views.vn_temple,name='vn_temple'),
    path('gallery_page',views.gallery_page,name='gallery_page'),
    # path('sub_album_page',views.sub_album_page,name='sub_album_page'),
    # path('all_sub_album_page',views.all_sub_album_page,name='all_sub_album_page'),
    path('jeeyars',views.jeeyars_parampara,name='jeeyars_parampara'),

    path('other_temple',views.other_temple,name='other_temple'),
    path('branches',views.branches,name='branches'),
    path('ponnadikkal_jeeyar',views.ponnadikkal_jeeyars,name='ponnadikkal_jeeyar'),
    path('jeeyars_details',views.jeeyars_details,name='jeeyars_details'),
    path('vn_education',views.vn_education,name='vn_education'),
    
    
    path('adminDashboard',admin_views.adminDashboard,name='adminDashboard'),
    path('home_page',admin_views.home_page,name='home_page'),
    path('addSectionLandingPage',admin_views.addSectionLandingPage,name='addSectionLandingPage'),
    path('vn_temple_edit',admin_views.vn_temple_edit,name='vn_temple_edit'),
    path('other_temple_edit',admin_views.other_temple_edit,name='other_temple_edit'),
    path('branches_edit',admin_views.branches_edit,name='branches_edit'),
    path('vn_education_edit',admin_views.vn_education_edit,name='vn_education_edit'),
    path('ponnadikkal_jeeyar_edit',admin_views.ponnadikkal_jeeyar_edit,name='ponnadikkal_jeeyar_edit'),
    path('jeeyars_edit',admin_views.jeeyars_edit,name='jeeyars_edit'),
    path('gallery_edit',admin_views.gallery_edit,name='gallery_edit'),


    path('adminAddNewTabData',admin_views.adminAddNewTabData,name='adminAddNewTabData'),
    path('addImageTabDataAdmin',admin_views.addImageTabDataAdmin,name='addImageTabDataAdmin'),
    path('addImageJeeyarAdmin',admin_views.addImageJeeyarAdmin,name='addImageJeeyarAdmin'),
    
    
    
    
    path('login',u_views.login,name='login'),
    
    
    path('',views.index,name='index'),
    path('newImageUpload',views.newImageUpload,name='newImageUpload'),
    path('fileDownload',views.fileDownload,name='newImageUpload'),
    
    
] +static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
