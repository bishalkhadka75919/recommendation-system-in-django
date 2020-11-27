from . import views
from django.conf.urls import url, include
from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'shop'


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('about/', views.about, name="about"),
    url('^', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace="social")),
    url('product_list/', views.product_list_category, name="list"),
    url('index/', views.index, name="shophome"),
    url(r'^$', views.index, name='product_list'),
    url('search/', views.search_list, name='query'),
    # url('electronics/', views.electronics, name='query'),
    url('trending/', views.search_list, name ='query'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list_category, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^cat/(?P<subcategory_slug>[-\w]+)/$', views.product_list_subcategory, name='product_list_by_subcategory'),

    url('r/reviewlist/', views.review_list, name='review_list'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^product$', views.product_list, name='product_list'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'^product/(?P<product_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$',views.user_review_list,name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    url('r/recommendation/', views.user_recommendation_list, name='user_recommendation_list'),



]




