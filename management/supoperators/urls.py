from django.urls import path
from . import views

app_name = 'supoperator'

urlpatterns = [
    path('', views.SupOperatorList.as_view(), name='index'),
    path('create/', views.SupOperatorCreate.as_view(), name='create'),
    path('edit/<int:pk>', views.SupOperatorCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.sup_operator_remove, name='remove')
]