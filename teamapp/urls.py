from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:article_id>/update', views.update, name='update'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/delete', views.delete, name='delete'),
    path('<int:article_id>/update', views.update, name='update'),
	path('<int:article_id>/like', views.like, name='like'),
	path('api/articles/<int:article_id>/like', views.api_like),
    path('bio', views.bio, name='bio'),
    path('detailscreen', views.detailscreen, name='detailscreen'),
    #path('home', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('create', views.user_create, name='create'),
    path('login/', auth_views.LoginView.as_view(template_name='teamapp/home_screen.html')),
]
