from django.urls import path
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchPost)

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPost.as_view(), name='post_list'),

   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('article/create', PostCreate.as_view(), name='article_create'),
   path('articles/update/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/delete/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
