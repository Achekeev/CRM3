from django.urls import path
from . import views

app_name = 'cammodel'

urlpatterns = [
    path('', views.CamModelList.as_view(), name='index'),
    path('create/', views.CamModelCreate.as_view(), name='create'),
    path('detail/<int:pk>', views.CamModelDetail.as_view(), name='detail'),
    path('edit/<int:pk>', views.CamModelCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.cammodel_remove, name='remove')
]