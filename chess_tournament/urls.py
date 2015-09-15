from django.conf.urls import include, url
from django.contrib import admin
from judge_interface import urls as judge_interface_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin_site_urls'),
    url('', include(judge_interface_urls), name='judge_interface_urls'),
]
