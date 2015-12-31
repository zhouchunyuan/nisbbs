from django.conf.urls import url

from . import views
app_name='wwrequests'
urlpatterns = [
    url(r'^$',views.view,name='index'),
    url(r'^discuss/(?P<reqid>[0-9]+)$',views.discuss_detail,name='detail'),
    url(r'^edit/(?P<reqid>[0-9]+)$',views.edit_req,name='edit'),
    url(r'^delete/(?P<reqid>[0-9]+)$',views.del_req,name='delete'),
    url(r'^viewVotes$',views.view_votes,name='see_vote'),
    url(r'^addRequest$',views.addWWRequest,name='add_req'),
    url(r'^vote$',views.vote,name='vote'),
    url(r'^uploadXLS$',views.uploadXLS,name='uploadXLS'),
    url(r'^downloadXLS$',views.downloadXLS,name='downloadXLS'),
    url(r'^logout$',views.logout_view,name='logout'),
]
