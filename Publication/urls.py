# urls.py
from django.urls import path , include
from . import views
from Comment.views import delete_comment,add_comment,update_comment
urlpatterns = [
    path('ajouter/', views.ajouter_publication, name='ajouter_publication'),
    path('list/', views.publication_liste, name='publication_liste'),
    path('<int:pk>/', views.publication_detail, name='publication_detail'),
    path('delete/<int:id>/', views.delete_publication, name='delete_publication'),
    path('update/<int:id>/', views.update_publication, name='update_publication'),
    path('comment/<int:publication_id>/update/<int:comment_id>/', views.update_comment, name='update_comment'),
    

    path('newsletter/subscribe/', views.subscribe_newsletter, name='newsletter_subscribe'),
    path('newsletter/confirm/<str:token>/', views.confirm_subscription, name='confirm_subscription'),
    path('share/<int:pk>/<str:platform>/', views.track_share, name='track_share'),
    path('rate/', views.rate_publication, name='rate_publication'),
    path('publication/rate/', views.rate_publication, name='rate_publication'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('delete-review/<int:rating_id>/', views.delete_review, name='delete_review'),
    path('export-pdf/<int:pk>/', views.export_publication_pdf, name='export_publication_pdf'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    









    #path('comment/update/<int:id>/', update_comment, name='update_comment'),
#path('comment/delete/<int:id>/',delete_comment, name='delete_comment'),
    #path('comment/add',add_comment, name='add_comment'),
    #path('comment/update/<int:id>/',update_comment, name='update_comment'),


    # Ajoutez d'autres routes ici
   
   
]
