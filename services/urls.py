from django.urls import path


from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services, name='index'),
    path('<slug:slug>/', views.service_detail, name='service'),
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product'),
]
