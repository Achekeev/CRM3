from django.urls import path
from . import views

app_name = 'supcammodel'

urlpatterns = [
    path('', views.SupCamModelList.as_view(), name='index'),
    path('create/', views.SupCamModelCreate.as_view(), name='create'),
    path('edit/<int:pk>', views.SupCamModelCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.sup_cammodel_remove, name='remove')
]
