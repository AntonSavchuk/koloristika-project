from django.urls import path


from . import views
from services import views as serv_views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('prices/', serv_views.product_price, name='price'),
]
