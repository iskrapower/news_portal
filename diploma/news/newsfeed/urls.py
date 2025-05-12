from django.urls import path
from newsfeed import views

app_name = 'newsfeed'

urlpatterns = [
    path('', views.IndexView.as_view(), name='article_list'),
    path('article/<int:id>', views.ArticleView.as_view(), name='article_detail'),
    path('article/create', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:id>/update', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:id>/delete', views.ArticleDeleteView.as_view(), name='article_delete'),
]
