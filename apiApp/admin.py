from django.contrib import admin
from apiApp.models import landing_page,vanamamalai_temple,gallery_album,gallery_details,gallery_youtube,gallery
from apiApp.models import vanamamalai_temple_tab
from apiApp.models import vanamamalai_other_temple,vanamamalai_other_temple_tab
from apiApp.models import jeeyars,jeeyars_tab
from apiApp.models import vanamamalai_mutt_branches,vanamamalai_mutt_branches_tab
from apiApp.models import vanamamalai_education,vanamamalai_education_tab
from apiApp.models import rootPageStatus

from apiApp.landing_page.landing_page_models import landing_page_flow,banner_section,facebook_section,small_banner,card_section,hero_section,suscribeModel,shishyaForm

# Register your models here.

admin.site.register(landing_page)
admin.site.register(vanamamalai_temple)
admin.site.register(gallery_album)
admin.site.register(gallery_details)
admin.site.register(gallery_youtube)
admin.site.register(gallery)
admin.site.register(jeeyars)
admin.site.register(vanamamalai_temple_tab)
admin.site.register(vanamamalai_other_temple)
admin.site.register(vanamamalai_other_temple_tab)
admin.site.register(jeeyars_tab)
admin.site.register(vanamamalai_mutt_branches)
admin.site.register(vanamamalai_mutt_branches_tab)
admin.site.register(vanamamalai_education)
admin.site.register(vanamamalai_education_tab)
admin.site.register(rootPageStatus)

admin.site.register(landing_page_flow)
admin.site.register(banner_section)
admin.site.register(facebook_section)
admin.site.register(small_banner)
admin.site.register(card_section)
admin.site.register(hero_section)
admin.site.register(suscribeModel)
admin.site.register(shishyaForm)
