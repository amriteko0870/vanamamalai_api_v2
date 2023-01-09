from django.db import models

# Create your models here.

class landing_page(models.Model):
    order = models.IntegerField(blank=True)
    h1 = models.CharField(max_length=2000,blank=True)
    h2 = models.CharField(max_length=2000,blank=True)
    p = models.CharField(max_length=2000,blank=True)
    img = models.TextField(blank=True)
    read_link = models.TextField(blank=True)
    yt_link = models.TextField(blank=True)
    file_link = models.TextField(blank=True)
    yt_title = models.CharField(max_length=2000,blank=True)
    file_title = models.CharField(max_length=2000,blank=True)
    layout = models.CharField(max_length=2000,blank=True)
    background_color = models.CharField(max_length=50,blank=True)
    show_status = models.BooleanField()

#-------------------------------------------------------------------------------
class vanamamalai_temple(models.Model):
    banner_image = models.TextField(blank=True)
    banner_heading = models.TextField(blank=True)
    content_title = models.TextField(blank=True)
    content_subtitle = models.TextField(blank=True)
    content_image = models.TextField(blank=True)
    show_status = models.BooleanField()

class vanamamalai_temple_tab(models.Model):
    temple_id = models.IntegerField(blank=True)
    tab_heading = models.TextField(blank=True)
    tab_desc = models.TextField(blank=True)
    show_status = models.BooleanField()

#----------------------------------------------------------------------------------
class vanamamalai_other_temple(models.Model):
    banner_image = models.TextField()
    banner_heading = models.TextField()
    content_title = models.TextField()
    content_subtitle = models.TextField()
    content_image = models.TextField()
    show_status = models.BooleanField()

class vanamamalai_other_temple_tab(models.Model):
    temple_id = models.IntegerField()
    tab_heading = models.TextField()
    tab_desc = models.TextField()
    show_status = models.BooleanField()

#-----------------------------------------------------------------------------------
class vanamamalai_mutt_branches(models.Model):
    banner_image = models.TextField()
    banner_heading = models.TextField()
    content_title = models.TextField()
    content_subtitle = models.TextField()
    content_image = models.TextField()
    show_status = models.BooleanField()

class vanamamalai_mutt_branches_tab(models.Model):
    branch_id = models.IntegerField()
    tab_heading = models.TextField()
    tab_desc = models.TextField()
    show_status = models.BooleanField()

#------------------------------------------------------------------------------------
class ponnadikkal_jeeyar(models.Model):
    banner_image = models.TextField()
    banner_heading = models.TextField()
    content_title = models.TextField()
    content_subtitle = models.TextField()
    content_image = models.TextField()
    show_status = models.BooleanField()

class ponnadikkal_jeeyar_tab(models.Model):
    jeeyar_id = models.IntegerField()
    tab_heading = models.TextField()
    tab_desc = models.TextField()
    show_status = models.BooleanField()

#------------------------------------------------------------------------------------
class thaniyans_and_vazhi_thirunamams(models.Model):
    pass

#------------------------------------------------------------------------------------
class vanamamalai_education(models.Model):
    banner_image = models.TextField()
    banner_heading = models.TextField()
    content_title = models.TextField()
    content_subtitle = models.TextField()
    content_image = models.TextField()
    show_status = models.BooleanField()

class vanamamalai_education_tab(models.Model):
    education_id = models.IntegerField()
    tab_heading = models.TextField()
    tab_desc = models.TextField()
    show_status = models.BooleanField()

#------------------------------------------------------------------------------------
class gallery_album(models.Model):
    album_name = models.TextField()
    show_status = models.BooleanField()
    
class gallery(models.Model):
    album_id = models.IntegerField(blank=True,null=True)
    image = models.TextField()
    name = models.TextField()
    details = models.TextField()


class gallery_details(models.Model):
    banner_image = models.TextField()
    banner_heading = models.TextField()


class gallery_youtube(models.Model):
    title = models.TextField()
    url = models.TextField()


#---------------------------------------------------------------------
class jeeyars(models.Model):
    name = models.TextField(blank=True)
    prefix = models.TextField(blank=True)
    start_date = models.TextField(blank=True)
    end_date = models.TextField(blank=True)
    jeeyar_no_suffix = models.TextField(blank=True)
    image = models.TextField(blank=True)
    jeeyar_no = models.IntegerField(blank=True,null=True)
    banner_image = models.TextField(blank=True)
    banner_heading = models.TextField(blank=True)
    show_status = models.BooleanField()


class jeeyars_tab(models.Model):
    jeeyar_id = models.IntegerField(blank=True)
    tab_heading = models.TextField(blank=True)
    tab_desc = models.TextField(blank=True)
    show_status = models.BooleanField()

# ------------------------------ Admin ---------------------------

class rootPageStatus(models.Model):
    title = models.TextField()
    show_status = models.BooleanField()