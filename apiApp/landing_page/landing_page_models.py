from django.db import models

class landing_page_flow(models.Model):
    section_layout = models.TextField(blank=True)
    show_status = models.BooleanField(blank=True)


class hero_section(models.Model): # layout 1
    h1 = models.TextField(blank=True)
    h2 = models.TextField(blank=True)
    img = models.TextField(blank=True)


# layout 2 from gallery youtube


class banner_section(models.Model): # layout 3
    type = models.TextField(blank=True)
    h1 = models.TextField(blank=True)
    p = models.TextField(blank=True)
    image = models.TextField(blank=True)
    section_id = models.TextField(blank=True)


class facebook_section(models.Model): # layout 4
    link = models.TextField(blank=True)


class small_banner(models.Model): # layout 5
    h1 = models.TextField(blank=True)
    p = models.TextField(blank=True)
    image = models.TextField(blank=True)
    section_id = models.TextField(blank=True)


class card_section(models.Model): # layout 6
    h1 = models.TextField(blank=True)
    p = models.TextField(blank=True)
    section_id = models.TextField(blank=True)

class suscribeModel(models.Model):
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    phone_no = models.TextField(blank=True)
    email = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    country = models.TextField(blank=True)