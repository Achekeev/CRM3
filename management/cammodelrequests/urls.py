from django.urls import path
from . import views

app_name = 'cammodelrequest'

urlpatterns = [
    path('', views.CamModelRequestList.as_view(), name='index'),
    path('detail/<int:pk>', views.CamModelRequestDetail.as_view(), name='detail'),
    path('create/<int:pk>', views.CamModelRequestCreateNewModel.as_view(), name='create'),
    path('remove/<int:pk>', views.cammodelrequest_remove, name='remove'),
]