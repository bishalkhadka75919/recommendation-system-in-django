from django.conf.urls  import url
from .import views
app_name = "reviews"
urlpatterns = [
    url(r'^$',views.review_list,name='review_list'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^wine$', views.wine_list, name='wine_list'),
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$',views.user_review_list,name='user_review_list'),
    url(r'^review/user/$',views.user_review_list,name='user_review_list'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
