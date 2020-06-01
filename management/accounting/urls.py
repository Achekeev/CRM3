from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.AccountingList.as_view(), name='index'),
    path('detail/<int:pk>', views.AccountingDetail.as_view(), name='detail'),
    path('createfromcammodel/<int:pk>', views.AccountingCamModelForm.as_view(), name='createfromcammodel'),
    path('createfromoperator/<int:pk>', views.AccountingOperatorForm.as_view(), name='createfromoperator'),
    path('model/<int:pk>', views.AccountingCamModelStatistics.as_view(), name='modelstatistics'),
    path('operator/<int:pk>', views.AccountingOperatorStatistics.as_view(), name='operatorstatistics'),
    path('remove/<int:pk>', views.daily_total_remove, name='remove')
]
