from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from views import (Register, AddRelatives,
                   AddRelationship, AddFamily, SearchRelatives, Login)

urlpatterns = [
    url(r'^v1/register/$', csrf_exempt(Register.as_view()), name='Information_register'),
    url(r'^v1/login/$', csrf_exempt(Login.as_view()), name='Information_login'),
    url(r'^v1/addfamily/$', csrf_exempt(AddFamily.as_view()), name='Information_addfamily'),
    url(r'^v1/addrelationship/$', csrf_exempt(AddRelationship.as_view()), name='Information_addrelationship'),
    url(r'^v1/addrelatives/$', csrf_exempt(AddRelatives.as_view()), name='Information_addrelatives'),
    url(r'^v1/searchrelative/$', csrf_exempt(SearchRelatives.as_view()), name='Information_searchrelatives'),
]