from django.urls import path
from .views import *


urlpatterns = [
    # path('', index, name='advertsement'),
    path('', AdvertsementListView.as_view(), name='advertsement_list'),
    path('create/', AdvertsementCreateView.as_view(), name='advertsement_create'),
    path('<int:pk>/', AdvertsementDetailView.as_view(), name='advertsement_detail'),
    path('<int:pk>/edit/', AdvertsementUpdateView.as_view(), name='advertsement_edit'),
    path('<int:pk>/delete/', AdvertsementDeleteView.as_view(), name='advertsement_delete'),
    path('user_advertsement/', AdvertsementsUserView.as_view(), name='advertsement_user'),
    path('user_replies/', RepliesUserListView.as_view(), name='replies_user'),
    path('user_replies/<int:pk>/', ReplyUserDetail.as_view(), name='reply_user_detail'),
    path('user_replies/<int:pk>/accept/', reply_accept, name='reply_accept'),
    path('user_replies/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('<int:pk>/create_replies/', RepliesAdvertsementCreate.as_view(), name='replies_advertsement'),
    path('news/', NewsCreate.as_view(), name='news_create'),
]

