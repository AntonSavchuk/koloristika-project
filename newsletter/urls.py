from django.urls import path

from . import views

app_name = 'newsletter'

urlpatterns = [
    path('create/', views.create_newsletter, name='create_newsletter'),
    path('list/', views.newsletter_list, name='newsletter_list'),
    path('preview/<int:newsletter_id>/', views.preview_newsletter, name='preview_newsletter'),
    path('edit/<int:newsletter_id>/', views.edit_newsletter, name='edit_newsletter'), 
    path('delete/<int:newsletter_id>/', views.delete_newsletter, name='delete_newsletter'), 
    # path('send/<int:newsletter_id>/', views.send_newsletter, name='send_newsletter'),
]