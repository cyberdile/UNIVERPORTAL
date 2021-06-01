from django.contrib.auth.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .models import LikeDislike, Post
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

#
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
        # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('', views.index, name='index'),
        path('accounts/success/', views.hello, name = 'hello'),
        path('register/', views.register, name = 'register'),
        path('posts/', views.post_list, name= 'post_list'),
        path('posts/next/<int:page_number>/', views.next_posts, name = 'next_posts'),
        path('posts/create/', views.post_create, name= 'post_create'),
        path('posts/<int:post_id>/', views.post_detail, name = 'post_detail'),
        path('posts/<int:post_id>/update/', views.post_update, name = 'post_update'),
        path('univer/', views.kaf_list, name= 'kaf_list'),
        path('univer/create/', views.kaf_create, name= 'kaf_create'),
        path('univer/<int:kaf_id>/update/', views.kaf_update, name= 'kaf_update'),
        path('univer/<int:kaf_id>/', views.kaf_detail, name= 'kaf_detail'),
        path('univer/<int:kaf_id>/groups/', views.group_list, name= 'group_list'),
        path('univer/<int:kaf_id>/groups/<int:group_id>/', views.group_detail, name= 'group_detail'),
        path('univer/<int:kaf_id>/groups/<int:group_id>/students/', views.student_list, name= 'student_list'),
        path('univer/<int:kaf_id>/groups/<int:group_id>/students/<int:student_id>/', views.student_detail, name= 'student_detail'),
        path('posts/<int:post_id>/like/', login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)), name='post_like'),
        path('posts/<int:post_id>/dislike/', login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)), name='post_dislike'),
        ]
