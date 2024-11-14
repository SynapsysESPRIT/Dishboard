from django.contrib import admin
from django.urls import path, include  
from django.conf.urls.static import static
from django.conf import settings
"""
URL configuration for Dishboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from Comment.views import CommentListView



urlpatterns = [
    path('', views.home, name='home'),  # Maps '/home' to the home view
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('Recette/', include("Recette.urls")),
    path('Publication/', include("Publication.urls")),
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('Article/', include('Article.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
