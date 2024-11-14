from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  *

urlpatterns = [

    path('', list ,name="list"),
    path('add/', AddArticle.as_view() , name="add"),
    path('details/', detailsClass, name='detailsClass'),
    path('update/', updateClass, name='updateArticle'),
    path('delete/<int:pk>/', DeleteArticle.as_view(), name='deleteArticle'),
    path('blog/', blog, name='blog'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)