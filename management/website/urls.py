from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.WebsiteList.as_view(), name='index'),
    path('create/', views.WebsiteCreate.as_view(), name='create'),
    path('edit/<int:pk>', views.WebsiteCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.website_remove, name='remove')
]