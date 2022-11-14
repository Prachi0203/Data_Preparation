
from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.index, name="index"),
    path('as_user/', views.as_user, name="as_user"),
    path('add_concept/', views.add_concept, name='add_concept'),
    path('view_concepts/', views.view_concepts, name='view_concepts'),
    path("edit_concept/<int:myid>/", views.edit_concept, name="edit_concept"),
    path('delete_concept/<int:myid>', views.delete_concept, name='delete_concept'),
    path('view_sentences/', views.view_sentences, name='view_sentences'),
    path('add_sentence/', views.add_sentence, name='add_sentence'),
    path('add_label/', views.add_label, name='add_label'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('delete_sentence/<int:myid>',
         views.delete_sentence, name='delete_sentence'),
    path('duplicate_sentence/<int:myid>',
         views.duplicate_sentence, name='duplicate_sentence'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('edit_sentence/<int:myid>', views.edit_sentence, name='edit_sentence')
]
