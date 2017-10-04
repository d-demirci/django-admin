from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from rest_framework.urlpatterns import format_suffix_patterns

from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView
from models import Sube, Dish
from forms import SubeForm, DishForm
from views import  SubeCreate, DishCreate,  SubeDetail, review, LoginRequiredCheckIsOwnerUpdateView, \
    APIDishDetail, APIDishList, APISubeDetail, APISubeList, APISubeReviewDetail, APISubeReviewList

urlpatterns = [
    # List latest 5 subes: /mysubes/
    url(r'^$',
        ListView.as_view(
            queryset=Sube.objects.filter(date__lte=timezone.now()).order_by('-date')[:5],
            context_object_name='latest_sube_list',
            template_name='mysubes/sube_list.html'),
        name='sube_list'),

    # Sube details, ex.: /mysubes/subes/1/
    url(r'^subes/(?P<pk>\d+)/$',
        SubeDetail.as_view(),
        name='sube_detail'),

    # Sube dish details, ex: /mysubes/subes/1/dishes/1/
    url(r'^subes/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Dish,
            template_name='mysubes/dish_detail.html'),
        name='dish_detail'),

    # Create a sube, /mysubes/subes/create/
    url(r'^subes/create/$',
        SubeCreate.as_view(),
        name='sube_create'),

    # Edit sube details, ex.: /mysubes/subes/1/edit/
    url(r'^subes/(?P<pk>\d+)/edit/$',
        LoginRequiredCheckIsOwnerUpdateView.as_view(
            model=Sube,
            form_class=SubeForm),
        name='sube_edit'),

    # Create a sube dish, ex.: /mysubes/subes/1/dishes/create/
    url(r'^subes/(?P<pk>\d+)/dishes/create/$',
        DishCreate.as_view(),
        name='dish_create'),

    # Edit sube dish details, ex.: /mysubes/subes/1/dishes/1/edit/
    url(r'^subes/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/edit/$',
        LoginRequiredCheckIsOwnerUpdateView.as_view(
            model=Dish,
            form_class=DishForm),
        name='dish_edit'),

    # Create a sube review, ex.: /mysubes/subes/1/reviews/create/
    url(r'^subes/(?P<pk>\d+)/reviews/create/$',
        review,
        name='review_create'),


]

urlpatterns += [
    # RESTful API
    url(r'^api/subes/$',
        APISubeList.as_view(), name='sube-list'),
    url(r'^api/subes/(?P<pk>\d+)/$',
        APISubeDetail.as_view(), name='sube-detail'),
    url(r'^api/dishes/$',
        login_required(APIDishList.as_view()), name='dish-list'),
    url(r'^api/dishes/(?P<pk>\d+)/$',
        APIDishDetail.as_view(), name='dish-detail'),
    url(r'^api/subereviews/$',
        APISubeReviewList.as_view(), name='subereview-list'),
    url(r'^api/subereviews/(?P<pk>\d+)/$',
        APISubeReviewDetail.as_view(), name='subereview-detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'xml'])
