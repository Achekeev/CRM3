from django.urls import path
from . import views

app_name = 'operator'

urlpatterns = [
    path('', views.OperatorList.as_view(), name='index'),
    path('create/', views.OperatorCreate.as_view(), name='create'),
    path('detail/<int:pk>', views.OperatorDetail.as_view(), name='detail'),
    path('edit/<int:pk>', views.OperatorCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.operator_remove, name='remove')
]