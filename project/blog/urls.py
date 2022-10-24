from django.urls import path
from .views import *


urlpatterns = [
   # path('', index, name='index'),
   # path('category/<int:category_id>', articles_by_category, name='category'),
   # path('article/<int:article_id>', article_detail, name='article_detail'),
   # path('add/', add_article, name='add')
   # если только лайки
   # path('add_or_delete_like/<int:article_id>', add_or_delete_like, name='like')

   path('', ArticleListView.as_view(), name='index'),
   path('category/<int:category_id>', ArticleByCategory.as_view(), name='category'),
   path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
   path('add/', NewArticle.as_view(), name='add'),
   path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),

   path('login/', user_login, name='login'),
   path('logout/', user_logout, name='logout'),
   path('about_site/', about_the_site, name='about_site'),
   path('about_developer/', about_the_developer, name='about_developer'),
   path('register/', register, name='register'),
   path('add_comment/<int:pk>/', save_comment, name='save_comment'),
   path('add_or_delete_mark/<int:article_id>/<str:action>/', add_or_delete_mark, name='mark'),
   path('search/', SearchResults.as_view(), name='search'),
   path('profile/', profile, name='profile'),

   path('change_user/', userEditView, name='change'),
   path('change_photo/', profile, name='change_photo'),
   path('delete_comment/<int:comment_id>/<int:article_id>', delete_comment, name='delete_comment')
]
